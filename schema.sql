CREATE TABLE contest ("contest_id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE , "start_time" DATETIME, "end_time" DATETIME, "name" TEXT NOT NULL , "company" TEXT NOT NULL , "short_description" TEXT NOT NULL ,"long_description" TEXT NOT NULL , "owner" INTEGER NOT NULL);
;
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE contest_questions (
    "question_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "contest_id" INTEGER NOT NULL,
    "owner" INTEGER NOT NULL,
    "question_name" TEXT NOT NULL,
    "question_string" TEXT NOT NULL
);
CREATE TABLE question_testcase (testcase_id INTEGER PRIMARY KEY, question_id INTEGER, test TEXT, answer TEXT, points INTEGER, time_limit REAL, space_limit INTEGER);
CREATE TABLE submission_testcase (id INTEGER PRIMARY KEY, testcase_id INTEGER, submission_id INTEGER, result_type INTEGER, result TEXT, run_time REAL, run_space INTEGER);
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
;
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
;
CREATE TABLE "question_comments" (
"comment_id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
"question_id" INTEGER  NOT NULL,
"user_id" INTEGER  NOT NULL,
"comment" TEXT  NOT NULL,
"time" DATETIME  NOT NULL
);
;
CREATE TABLE "answer_comments" (
"comment_id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
"submission_id" INTEGER  NOT NULL,
"user_id" INTEGER  NOT NULL,
"comment" TEXT  NOT NULL,
"time" DATETIME  NOT NULL
);
;
CREATE TABLE "question_discuss" (
"question_id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
"user_id" INTEGER  NOT NULL,
"question" TEXT  NOT NULL,
"time" DATETIME  NOT NULL
);
;
CREATE TABLE "answer_discuss" (
"answer_id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
"user_id" INTEGER  NOT NULL,
"question_id" INTEGER  NOT NULL,
"answer" TEXT  NOT NULL,
"time" DATETIME  NOT NULL
);
;
CREATE TABLE submissions (
    "points" INTEGER,
    "lang" TEXT,
    "code" TEXT,
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "user_id" INTEGER,
    "submission_time" DATETIME,
    "question_id" INTEGER DEFAULT (0)
);
CREATE TABLE activity_log (
    "activity_id" INTEGER NOT NULL,
    "user_id" INTEGER NOT NULL,
    "activity" TEXT NOT NULL,
    "time" DATETIME NOT NULL
, "url" TEXT);
