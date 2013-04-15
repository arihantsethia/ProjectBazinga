CREATE TABLE contest ("contest_id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE , "start_time" DATETIME, "end_time" DATETIME, "name" TEXT NOT NULL , "company" TEXT NOT NULL , "short_description" TEXT NOT NULL ,"long_description" TEXT NOT NULL , "owner" INTEGER NOT NULL);
CREATE TABLE contest_questions (
    "question_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "contest_id" INTEGER NOT NULL,
    "owner" INTEGER NOT NULL,
    "question_name" TEXT NOT NULL,
    "question_string" TEXT NOT NULL
);
CREATE TABLE question_testcase (testcase_id INTEGER PRIMARY KEY, question_id INTEGER, test TEXT, answer TEXT, points INTEGER, time_limit REAL, space_limit INTEGER);
CREATE TABLE submission_testcase (id INTEGER PRIMARY KEY, testcase_id INTEGER, submission_id INTEGER, result_type INTEGER, result TEXT, run_time REAL, run_space INTEGER);
CREATE TABLE submissions (points INTEGER, lang TEXT, code TEXT, id INTEGER PRIMARY KEY, user_id INTEGER, submission_time DATETIME);
CREATE TABLE "follow" ("follower" INTEGER, "following" INTEGER);
CREATE TABLE "history" ("user_id" INTEGER, "q_id" INTEGER, "status" TEXT DEFAULT Accepted);
CREATE TABLE "users" (
    "user_id" INTEGER PRIMARY KEY NOT NULL,
    "username" TEXT UNIQUE NOT NULL,
    "password" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "contact" TEXT,
    "profession" TEXT,
    "organization" TEXT,
    "website" TEXT,    
    "picture" BLOB,
    "resume" BLOB
);
CREATE TABLE "admins" (
    "admin_id" INTEGER PRIMARY KEY NOT NULL,
    "username" TEXT UNIQUE NOT NULL,
    "password" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "contact" TEXT,
    "organization" TEXT,
    "website" TEXT,    
    "picture" BLOB
);
CREATE TABLE "question_comments" (
"comment_id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
"question_id" INTEGER  NOT NULL,
"user_id" INTEGER  NOT NULL,
"comment" TEXT  NOT NULL,
"time" DATETIME  NOT NULL
);


CREATE TABLE "answer_comments" (
"comment_id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
"submission_id" INTEGER  NOT NULL,
"user_id" INTEGER  NOT NULL,
"comment" TEXT  NOT NULL,
"time" DATETIME  NOT NULL
);

CREATE TABLE "question_discuss" (
"question_id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
"user_id" INTEGER  NOT NULL,
"question" TEXT  NOT NULL,
"time" DATETIME  NOT NULL
);

CREATE TABLE "answer_discuss" (
"answer_id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
"user_id" INTEGER  NOT NULL,
"question_id" INTEGER  NOT NULL,
"answer" TEXT  NOT NULL,
"time" DATETIME  NOT NULL
);

CREATE TABLE "activity_log" (
"activity_id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
"user_id" INTEGER  NOT NULL,
"activity" TEXT  NOT NULL,
"time" DATETIME  NOT NULL
);
CREATE TABLE "contact" (
"activity_id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
"user_id" INTEGER  NOT NULL,
"activity" TEXT  NOT NULL,
"time" DATETIME  NOT NULL
)
INSERT INTO admins VALUES(0,'arihant','arihant','arihantsethia07@gmail.com','Arihant Sethia','8011244745','IIT Guwahati','github.com','picture.img');
INSERT INTO users VALUES(0,'arihant','arihant','arihantsethia07@gmail.com','Arihant Sethia','8011244745','Student','IIT G','github.com','picture.img','resume.pdf');
INSERT INTO contest VALUES(0,'1990-1-1 00:00:00','2099-1-1 00:00:00','Practice','Bazinga','Hone your skills',"Long Description Here",0);
INSERT INTO contest VALUES(1,'1995-1-1 00:00:00','2014-1-1 00:00:00','InterIIT','Bazinga','Inter IIT coding challenge',"Long Description Here",0);
INSERT INTO contest VALUES(2,'1995-1-1 00:00:00','2011-1-1 00:00:00','CodeSprint','Bazinga','Death Race',"Long Description Here",0);
INSERT INTO contest_questions VALUES(1,0,0,'Primes','Generate the first 6 prime numbers');
INSERT INTO contest_questions VALUES(2,0,0,'Primes2','Generate the first 6 prime numbers (2)');
INSERT INTO contest_questions VALUES(3,0,0,'Primes3','Generate the first 6 prime numbers (3)');
INSERT INTO contest_questions VALUES(4,1,0,'Primes','Generate the first 6 prime numbers');
INSERT INTO contest_questions VALUES(5,1,0,'Primes2','Generate the first 6 prime numbers (2)');
INSERT INTO contest_questions VALUES(6,1,0,'Primes3','Generate the first 6 prime numbers (3)');
INSERT INTO contest_questions VALUES(7,2,0,'Primes','Generate the first 6 prime numbers');
INSERT INTO contest_questions VALUES(8,2,0,'Primes2','Generate the first 6 prime numbers (2)');
INSERT INTO contest_questions VALUES(9,2,0,'Primes3','Generate the first 6 prime numbers (3)');
INSERT INTO question_testcase VALUES(1,1,'hello','hello',10,200.0,6000000);
INSERT INTO sqlite_sequence VALUES('contest',6);
INSERT INTO sqlite_sequence VALUES('contest_questions',18);
INSERT INTO submission_testcase VALUES(1,1,1,10,'',0.0,0);
INSERT INTO submissions VALUES(10,'c','#include <stdio.h>
int main(){
printf("hello");
return 0;
}',1,0,'2013-03-29 16:35:09');

