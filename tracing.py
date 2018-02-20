import telebot
import time
import config
import parser

from db_interface import DBInterface

class Trace:
    def __init__(self):
        self.message = "hi"
        self.bot = telebot.TeleBot(config.token)

    def check(self):
        with DBInterface(config.database_name) as db:
            courses = db.get_courses()
        for course_id, old_name, old_last_check, old_busy, old_places in courses:
            old_full = (old_busy >= old_places)
            new_id, new_name, new_busy, new_places = parser.get_course_info(str(course_id))
            t = time.time()
            with DBInterface(config.database_name) as db:
                db.add_course(new_id, new_name, new_busy, new_places, t)
            if new_name != old_name:
                self.notice_change_name(course_followers)
            if new_busy >= new_places:
                continue
            with DBInterface(config.database_name) as db:
                course_followers = db.get_course_chats(new_id) 
            self.notification(old_full, new_busy, new_places, course_followers)
            

    def notification(self, old_full, busy, places, course_followers):
        if old_full and (busy < places):  
            for course_name, chat_id, add_time, in course_followers:
                self.bot.send_message(chat_id,
                    config.md_mes(config.course_not_full_message % (course_name, busy, places)))
                
if __name__ == '__main__':
    tr = Trace()
    tr.check()
