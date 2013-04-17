CREATE TABLE contest ("contest_id" INTEGER PRIMARY KEY  AUTOINCREMENT    UNIQUE , "start_time" DATETIME, "end_time" DATETIME, "name" TEXT  , "company" TEXT , "short_description" TEXT  ,"long_description" TEXT  , "owner" INTEGER );
CREATE TABLE contest_questions (
    "question_id" INTEGER PRIMARY KEY AUTOINCREMENT ,
    "contest_id" INTEGER ,
    "owner" INTEGER ,
    "question_name" TEXT ,
    "question_string" TEXT 
);
CREATE TABLE question_testcase (testcase_id INTEGER PRIMARY KEY AUTOINCREMENT , question_id INTEGER, test TEXT, answer TEXT, points INTEGER, time_limit REAL, space_limit INTEGER);
CREATE TABLE submission_testcase (id INTEGER PRIMARY KEY AUTOINCREMENT , testcase_id INTEGER, submission_id INTEGER, result_type INTEGER, result TEXT, run_time REAL, run_space INTEGER);
CREATE TABLE "follow" ("follower" INTEGER, "following" INTEGER);
CREATE TABLE "history" ("user_id" INTEGER, "q_id" INTEGER, "status" TEXT DEFAULT Accepted);
CREATE TABLE "users" (
    "user_id" INTEGER PRIMARY KEY AUTOINCREMENT ,
    "username" TEXT ,
    "password" TEXT ,
    "email" TEXT ,
    "name" TEXT ,
    "contact" TEXT,
    "profession" TEXT,
    "organization" TEXT,
    "website" TEXT
);
CREATE TABLE "admins" (
    "admin_id" INTEGER PRIMARY KEY AUTOINCREMENT ,
    "username" TEXT ,
    "password" TEXT ,
    "email" TEXT ,
    "name" TEXT ,
    "contact" TEXT,
    "organization" TEXT,
    "website" TEXT,    
    "picture" BLOB
);
CREATE TABLE "question_comments" (
"comment_id" INTEGER PRIMARY KEY AUTOINCREMENT ,
"question_id" INTEGER  ,
"user_id" INTEGER  ,
"comment" TEXT  ,
"time" DATETIME  
);
CREATE TABLE "answer_comments" (
"comment_id" INTEGER PRIMARY KEY AUTOINCREMENT ,
"submission_id" INTEGER  ,
"user_id" INTEGER  ,
"comment" TEXT  ,
"time" DATETIME  
);
CREATE TABLE "answer_discuss" (
"answer_id" INTEGER PRIMARY KEY AUTOINCREMENT ,
"user_id" INTEGER  ,
"question_id" INTEGER  ,
"answer" TEXT  ,
"time" DATETIME  
);
CREATE TABLE submissions (
    "points" INTEGER,
    "lang" TEXT,
    "code" TEXT,
    "id" INTEGER PRIMARY KEY AUTOINCREMENT ,
    "user_id" INTEGER,
    "submission_time" DATETIME,
    "question_id" INTEGER DEFAULT (0)
);
CREATE TABLE activity_log (
    "activity_id" INTEGER PRIMARY KEY AUTOINCREMENT ,
    "user_id" INTEGER ,
    "activity" TEXT ,
    "time" DATETIME 
, "url" TEXT);
CREATE TABLE question_discuss (
    "question_id" INTEGER PRIMARY KEY AUTOINCREMENT ,
    "user_id" INTEGER ,
    "question" TEXT ,
    "time" DATETIME 
, "title" TEXT);