-- https://onecompiler.com/mysql/3zrdm34wh
-- create
CREATE TABLE EMPLOYEE (
  empId INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  dept TEXT NOT NULL
);
CREATE TABLE SECRECT(
  idkey INTEGER PRIMARY KEY,
  value TEXT NOT NULL
);
CREATE TABLE USERS(
  idkey INTEGER PRIMARY KEY,
  user TEXT NOT NULL,
  pass TEXT NOT NULL
);
-- insert
INSERT INTO EMPLOYEE VALUES (0001, 'Clark', 'Sales');
INSERT INTO EMPLOYEE VALUES (0002, 'Dave', 'Accounting');
INSERT INTO EMPLOYEE VALUES (0003, 'Ava', 'Sales');
INSERT INTO EMPLOYEE VALUES (0004, 'Clark', 'Sales');
INSERT INTO EMPLOYEE VALUES (0005, 'Dave', 'Accounting');
INSERT INTO EMPLOYEE VALUES (0006, 'Ava', 'Sales');

INSERT INTO SECRECT VALUES (0001, 'abc');
INSERT INTO USERS VALUES (0001, 'adminstator','12345678');

SELECT (SUBSTRING((SELECT table_name FROM information_schema.tables WHERE table_schema=database() LIMIT 1 ),1,1));
-- fetch 
-- SELECT 'before DELETE' as '';
-- SELECT * FROM EMPLOYEE;
-- DELETE FROM EMPLOYEE WHERE empId=0001;
-- SELECT 'DELETE 1' as '';
-- SELECT * FROM EMPLOYEE;
-- DELETE FROM EMPLOYEE WHERE empId=0006 OR (SELECT 'a' FROM SECRECT LIMIT 1)='a';
-- SELECT 'TEST ALL' as '';
-- SELECT 'a' FROM SECRECT LIMIT 1;
-- SELECT 'DELETE ALL' as '';
-- SELECT * FROM EMPLOYEE;
-- SELECT 'CHECK VERSIOn' as '';
-- SELECT @@version
-- SELECT (ASCII(SUBSTRING((SELECT GROUP_CONCAT(table_name) FROM information_schema.tables WHERE table_schema = database()), 1, 1)));
-- SELECT ASCII(SUBSTRING((SELECT table_name FROM information_schema.tables WHERE table_schema=database());,1,1)) 
SELECT 'before DELETE' as '';SELECT * FROM EMPLOYEE;
-- DELETE FROM EMPLOYEE WHERE empId=0001 OR (SUBSTRING((SELECT table_name FROM information_schema.tables WHERE table_schema=database() LIMIT 1 ),1,1)) < 'a';
SELECT 'AFTER DELETE' as '';SELECT * FROM EMPLOYEE;
-- SELECT (Ascii(substring((SELECT table_name FROM information_schema.tables WHERE table_schema = database() LIMIT 0,1),1,1)));
SELECT table_name FROM information_schema.tables WHERE table_schema=database();
SELECT (LENGTH((SELECT GROUP_CONCAT(table_name) FROM information_schema.tables WHERE table_schema=database() LIMIT 1 )));
-- SELECT ASCII('U');

SELECT (SUBSTRING((SELECT GROUP_CONCAT(COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'employee'),1,1))
-- SELECT table_name FROM information_schema.tables WHERE table_schema=database() LIMIT 1;
-- SELECT 'TEST VULN' as '';SELECT * FROM EMPLOYEE;
-- SELECT 'u' FROM users WHERE user='administrator';
-- SELECT 'u' FROM users WHERE user='adminstator'

-- (ASCII(SUBSTRING((SELECT GROUP_CONCAT(table_name) FROM information_schema.tables WHERE table_schema=database()),1,1)))=101;