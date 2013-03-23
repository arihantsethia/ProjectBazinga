CREATE TABLE contest ("contest_id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE , "start_time" DATETIME, "end_time" DATETIME, "name" TEXT NOT NULL , "company" TEXT NOT NULL , "description" TEXT NOT NULL );
;
CREATE TABLE submissions (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "user_id" INTEGER NOT NULL,
    "submission_id" INTEGER NOT NULL,
    "result_id" INTEGER NOT NULL,
    "result" TEXT NOT NULL,
    "submission_time" DATETIME NOT NULL,
    "run_time" TIME NOT NULL,
    "run_space" INTEGER NOT NULL
);
CREATE TABLE question_testcase (
    "testcase_id" INTEGER NOT NULL,
    "question_id" INTEGER NOT NULL,
    "test" TEXT NOT NULL,
    "answer" TEXT NOT NULL,
    "point" REAL NOT NULL,
    "time_limit" TIME NOT NULL,
    "space_limit" INTEGER NOT NULL
);
CREATE TABLE contest_questions (
    "question_id" INTEGER NOT NULL,
    "contest_id" INTEGER NOT NULL,
    "user_id" INTEGER NOT NULL,
    "question_name" TEXT NOT NULL,
    "question_string" TEXT NOT NULL
);
