-- SQLite

--Enable foreign key support
PRAGMA foreign_keys;
PRAGMA foreign_keys = ON;
PRAGMA foreign_keys;

--Start new transaction
BEGIN TRANSACTION;

--Create the Job table and define the data characteristics of the columns
CREATE TABLE JOB(JOB_CODE CHAR(3) PRIMARY KEY,
JOB_DESCRIPTION VARCHAR(30));

--Insert sample data into the Job table
INSERT INTO JOB (JOB_CODE, JOB_DESCRIPTION) VALUES
('A01', 'Software Developer'),
('A02', 'Database Administrator'),
('A03', 'Systems Analyst'),
('A04', 'Network Engineer'),
('A05', 'Project Manager'),
('A06', 'Clerk 1'),
('A07', 'Clerk 2');

--Create the Employee table and define the data characteristics of the columns
CREATE TABLE EMPLOYEE(EMP_ID CHAR(3) PRIMARY KEY,
LAST_NAME VARCHAR(15) NOT NULL,
FIRST_NAME VARCHAR(15) NOT NULL,
INITIAL CHAR(1),
HIRE_DATE DATE,
JOB_CODE CHAR(3) NOT NULL,
FOREIGN KEY(JOB_CODE) REFERENCES JOB(JOB_CODE) ON DELETE CASCADE);

--Insert sample data into the Employee table
INSERT INTO EMPLOYEE (EMP_ID, LAST_NAME, FIRST_NAME, INITIAL, HIRE_DATE, JOB_CODE) VALUES
('E01', 'Smith',   'John',   'A', '2020-03-15', 'A01'),
('E02', 'Johnson', 'Emily',  'B', '2019-07-22', 'A02'),
('E03', 'Davis',   'Michael','C', '2021-01-10', 'A03'),
('E04', 'Martinez','Sophia', 'D', '2018-11-05', 'A04'),
('E05', 'Brown',   'David',  'E', '2022-06-30', 'A05'),
('E06', 'Smith','Kevin', 'P', '1994-10-19', 'A06'),
('E07', 'Mewes','Jason', 'E', '2006-07-21', 'A07');

--Save preceding steps to disk
COMMIT;