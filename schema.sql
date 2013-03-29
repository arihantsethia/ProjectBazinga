BEGIN TRANSACTION;
CREATE TABLE contest ("contest_id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE , "start_time" DATETIME, "end_time" DATETIME, "name" TEXT NOT NULL , "company" TEXT NOT NULL , "description" TEXT NOT NULL , "owner" INTEGER NOT NULL);
INSERT INTO contest VALUES(0,'1990-1-1 00:00:00','2099-1-1 00:00:00','Practice','Bazinga','Hone your skills',0);
INSERT INTO contest VALUES(1,'1995-1-1 00:00:00','2014-1-1 00:00:00','InterIIT','Bazinga','Inter IIT coding challenge',0);
INSERT INTO contest VALUES(2,'1995-1-1 00:00:00','2011-1-1 00:00:00','CodeSprint','Bazinga','Death Race',0);
CREATE TABLE contest_questions (
    "question_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "contest_id" INTEGER NOT NULL,
    "owner" INTEGER NOT NULL,
    "question_name" TEXT NOT NULL,
    "question_string" TEXT NOT NULL
);
INSERT INTO contest_questions VALUES(1,0,0,'Primes','Generate the first 6 prime numbers');
INSERT INTO contest_questions VALUES(2,0,0,'Primes2','Generate the first 6 prime numbers (2)');
INSERT INTO contest_questions VALUES(3,0,0,'Primes3','Generate the first 6 prime numbers (3)');
INSERT INTO contest_questions VALUES(4,1,0,'Primes','Generate the first 6 prime numbers');
INSERT INTO contest_questions VALUES(5,1,0,'Primes2','Generate the first 6 prime numbers (2)');
INSERT INTO contest_questions VALUES(6,1,0,'Primes3','Generate the first 6 prime numbers (3)');
INSERT INTO contest_questions VALUES(7,2,0,'Primes','Generate the first 6 prime numbers');
INSERT INTO contest_questions VALUES(8,2,0,'Primes2','Generate the first 6 prime numbers (2)');
INSERT INTO contest_questions VALUES(9,2,0,'Primes3','Generate the first 6 prime numbers (3)');
CREATE TABLE question_testcase (testcase_id INTEGER PRIMARY KEY, question_id INTEGER, test TEXT, answer TEXT, points INTEGER, time_limit REAL, space_limit INTEGER);
INSERT INTO question_testcase VALUES(1,1,'hello','hello',10,200.0,6000000);
CREATE TABLE sqlite_sequence(name,seq);
INSERT INTO sqlite_sequence VALUES('contest',6);
INSERT INTO sqlite_sequence VALUES('contest_questions',18);
CREATE TABLE submission_testcase (id INTEGER PRIMARY KEY, testcase_id INTEGER, submission_id INTEGER, result_type INTEGER, result TEXT, run_time REAL, run_space INTEGER);
INSERT INTO submission_testcase VALUES(1,1,1,10,'',0.0,0);
CREATE TABLE submissions (points INTEGER, lang TEXT, code TEXT, id INTEGER PRIMARY KEY, user_id INTEGER, submission_time DATETIME);
INSERT INTO submissions VALUES(10,'c','#include <stdio.h>
int main(){
printf("hello");
return 0;
}',1,0,'2013-03-29 16:35:09');
COMMIT;
