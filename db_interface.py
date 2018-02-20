import sqlite3

class DBInterface:

    def __init__(self,database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self,exp_type, exp_value, exp_tr):
        self.close()

    def add_chat(self,chat_id):
        with self.connection:
            self.cursor.execute("INSERT OR IGNORE INTO chats VALUES (?)",(chat_id,))

    def add_course(self,course_id,course_name,busy,places,add_time,replace = True):
        with self.connection:
            course = self.cursor.execute(
            "SELECT * FROM courses WHERE course_id={} LIMIT 1".format(course_id)) \
            .fetchall()
            if course and replace:
                self.cursor.execute(
                "REPLACE INTO courses VALUES (?,?,?,?,?)",
                (course_id,course_name,add_time,busy,places))
                return (course_id,course_name,add_time,busy,places)
            elif course and not replace:
                return course[0]
            elif not course:
                self.cursor.execute(
                "INSERT INTO courses VALUES (?,?,?,?,?)",
                (course_id,course_name,add_time,busy,places))
                return (course_id,course_name,add_time,busy,places)

    def follow(self,chat_id,course_id,add_time):
        with self.connection:
            self.cursor.execute(
                "INSERT OR REPLACE INTO chat_course VALUES (?,?,?)",
                (course_id,chat_id,add_time))
        return True
    

    def get_courses(self):
        with self.connection:
            courses = self.cursor.execute("SELECT * FROM courses ORDER BY last_check ASC").fetchall()
        return courses

    def get_course_chats(self,course_id):
        with self.connection:
            chats = self.cursor.execute("SELECT * from chat_course where course_id = {} ORDER BY add_time ASC"\
                .format(course_id)).fetchall()
        return chats

    def unfollow(self,course_id,chat_id):
        with self.connection:
            # course = self.cursor.execute(
            # "SELECT * FROM chat_course WHERE course_id={} LIMIT 1".format(course_id)) \
            # .fetchall()
            rows = self.cursor.execute("DELETE FROM chat_course WHERE course_id = {} and chat_id = {}"\
                .format(course_id,chat_id)).rowcount
            if not rows:
                return False
            if not self.get_course_chats(course_id):
                self.cursor.execute("DELETE FROM courses WHERE course_id = {}"\
                    .format(course_id))
            # except 
        return True

    def get_chat_courses(self,chat_id):
        with self.connection:
            courses = self.cursor.execute("""SELECT * from courses where course_id IN 
             (SELECT course_id FROM chat_course WHERE chat_id = {}) 
             ORDER BY last_check ASC"""\
                .format(chat_id)).fetchall()
        return courses


    def close(self):
        self.connection.close()