
CREATE TABLE chats (
	chat_id	INTEGER PRIMARY KEY
);

CREATE TABLE courses (
	course_id INTEGER PRIMARY KEY,
	name TEXT NOT NULL,
	last_check INTEGER NOT NULL,
	busy INTEGER NOT NULL,
	places INTEGER NOT NULL,
);

CREATE TABLE chat_course (
	course_id INTEGER NOT NULL,
	chat_id	INTEGER NOT NULL,
	add_time NOT NULL,
	FOREIGN KEY (course_id) REFERENCES courses(course_id),
	FOREIGN KEY (chat_id)   REFERENCES chats(chat_id)
);

