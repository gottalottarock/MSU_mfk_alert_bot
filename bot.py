# -*- coding: utf-8 -*-
import config
import telebot
import parser
from db_interface import DBInterface
import time
from sqlite3 import DatabaseError
bot = telebot.TeleBot(config.token)

def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            bot.send_message(m.chat.id, m.text)

@bot.message_handler(commands=["start"])
def start_handler(message):
    answer = '\n'.join([config.hello_message, config.help_message])
    with DBInterface(config.database_name) as db:
        db.add_chat(message.chat.id)
    bot.send_message(message.chat.id,**config.md_mes(answer))


@bot.message_handler(commands=["help"])
def help_handler(message):
    bot.send_message(message.chat.id,**config.md_mes( config.help_message))

@bot.message_handler(commands=['check'])
def check_handler(message):
    if len(message.text.split())>=1:
        answers = []
        for mes in message.text.split()[1:]:
            try:
                ans = parser.get_course_info(mes)
            except (parser.WebExeption, parser.URLExeption):
                bot.send_message(message.chat.id,**config.md_mes(
                    config.parser_error_message))
                return
            answers.append(config.check_message % ans[1:])
        answer = '\n'.join(answers)
        bot.send_message(message.chat.id,**config.md_mes(answer))
    else:
        bot.send_message(message.chat.id,**config.md_mes(config.no_link_error))

@bot.message_handler(commands=['follow'])
def follow_handler(message):
    try:
        if len(message.text.split())>=1:
            for mes in message.text.split()[1:]:
                course_info = parser.get_course_info(mes)
                t = time.time() 
                with DBInterface(config.database_name) as db:
                    db = DBInterface(config.database_name)
                    db.add_course(*course_info,add_time=t)
                    db.follow(message.chat.id,course_info[0],t)
                bot.send_message(message.chat.id,
                    **config.md_mes(config.successful_follow_message % course_info[1:]))
        else:
            bot.send_message(message.chat.id,**config.md_mes(config.no_link_error))
    except DatabaseError as e:
        bot.send_message(message.chat.id, **config.md_mes(config.database_error_message))
        print(str(e))

@bot.message_handler(commands=['unfollow'])
def unfollow_handler(message):
    try:
        if len(message.text.split())>=1:
            for mes in message.text.split()[1:]:
                course_info = parser.get_course_info(mes)
                with DBInterface(config.database_name) as db:
                    res = db.unfollow(course_info[0], message.chat.id)
                    if res:
                        bot.send_message(message.chat.id, **config.md_mes(
                            config.successful_unfollow_message % course_info[1]))
                    else:
                        bot.send_message(message.chat.id, **config.md_mes(
                            config.not_following_message % course_info[1]))
        else:
            bot.send_message(message.chat.id,**config.md_mes(config.no_link_error))

    except DatabaseError as e:
        bot.send_message(message.chat.id, **config.md_mes(config.database_error_message))
        print(str(e))

@bot.message_handler(commands = ['status'])
def status_message(message):
    with DBInterface(config.database_name) as db:
        courses = db.get_chat_courses(message.chat.id)
    if not courses:
        bot.send_message(message.chat.id,**config.md_mes(config.no_courses_message))
        return
    bot.send_message(message.chat.id,**config.md_mes(format_status(courses)))



@bot.message_handler(commands =['my_id'])
def my_id_handler(message):
    bot.send_message(message.chat.id,**config.md_mes(str(message.chat.id)))

# def md_mes(mes):
#     return {'text':mes, 'parse_mode':"Markdown"}

def format_time(now,old):
    dt = now-old
    str_t = time.strftime('%M мин %S c', time.gmtime(dt))
    return str_t

def format_status(courses):
    ans = []
    t = time.time()
    for c in courses:
        ans.append(config.status_message.format(c[1],format_time(t,c[2]),c[3],c[4]))
    return '\n'.join(ans)

if __name__ == '__main__':
    bot.set_update_listener(listener)
    bot.polling(none_stop=True)

url = 'https://iplogger.ru/logger/kyed3frCN3/'