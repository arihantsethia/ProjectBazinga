CREATE TABLE IF NOT EXISTS contest ("contest_id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE , "start_time" DATETIME, "end_time" DATETIME, "name" TEXT NOT NULL , "company" TEXT NOT NULL , "description" TEXT NOT NULL , "owner" INTEGER NOT NULL);
;
CREATE TABLE IF NOT EXISTS submissions (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "user_id" INTEGER NOT NULL,
    "submission_id" INTEGER NOT NULL,
    "result_id" INTEGER NOT NULL,
    "result" TEXT NOT NULL,
    "submission_time" DATETIME NOT NULL,
    "run_time" TIME NOT NULL,
    "run_space" INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS question_testcase (
    "testcase_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "question_id" INTEGER NOT NULL,
    "test" TEXT NOT NULL,
    "answer" TEXT NOT NULL,
    "points" REAL NOT NULL,
    "time_limit" TIME NOT NULL,
    "space_limit" INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS contest_questions (
    "question_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "contest_id" INTEGER NOT NULL,
    "owner" INTEGER NOT NULL,
    "question_name" TEXT NOT NULL,
    "question_string" TEXT NOT NULL
);

INSERT INTO contest (name, start_time, end_time, company, description, owner) VALUES ("Practice", "1990-1-1 00:00:00", "2099-1-1 00:00:00", "Bazinga", "Hone your skills", 0);
INSERT INTO contest (name, start_time, end_time, company, description, owner) VALUES ("InterIIT", "1995-1-1 00:00:00", "2014-1-1 00:00:00", "Bazinga", "Inter IIT coding challenge", 0);
INSERT INTO contest (name, start_time, end_time, company, description, owner) VALUES ("CodeSprint", "1995-1-1 00:00:00", "2014-1-1 00:00:00", "Bazinga", "Death Race", 0);

INSERT INTO contest_questions (contest_id, owner, question_name, question_string)
                       VALUES (0, 0, "Primes", "Generate the first 6 prime numbers");
INSERT INTO contest_questions (contest_id, owner, question_name, question_string)
                       VALUES (0, 0, "Primes2", "Generate the first 6 prime numbers (2)");
INSERT INTO contest_questions (contest_id, owner, question_name, question_string)
                       VALUES (0, 0, "Primes3", "Generate the first 6 prime numbers (3)");

INSERT INTO contest_questions (contest_id, owner, question_name, question_string)
                       VALUES (1, 0, "Primes", "Generate the first 6 prime numbers");
INSERT INTO contest_questions (contest_id, owner, question_name, question_string)
                       VALUES (1, 0, "Primes2", "Generate the first 6 prime numbers (2)");
INSERT INTO contest_questions (contest_id, owner, question_name, question_string)
                       VALUES (1, 0, "Primes3", "Generate the first 6 prime numbers (3)");

INSERT INTO contest_questions (contest_id, owner, question_name, question_string)
                       VALUES (2, 0, "Primes", "Generate the first 6 prime numbers");
INSERT INTO contest_questions (contest_id, owner, question_name, question_string)
                       VALUES (2, 0, "Primes2", "Generate the first 6 prime numbers (2)");
INSERT INTO contest_questions (contest_id, owner, question_name, question_string)
                       VALUES (2, 0, "Primes3", "Generate the first 6 prime numbers (3)");
