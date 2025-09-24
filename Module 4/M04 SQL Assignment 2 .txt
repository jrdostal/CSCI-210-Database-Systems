--sqlite

--Start new transaction
BEGIN TRANSACTION;

--Update Job Code for an employee
UPDATE EMPLOYEE SET JOB_CODE = "A02" WHERE EMP_ID = "E03";

--Deleting the row for an employee who was terminated
DELETE FROM EMPLOYEE WHERE HIRE_DATE = "2018-11-05";

--Select statement to show all employees by last name
SELECT * FROM EMPLOYEE ORDER BY LAST_NAME;

--Select statement to show all employees with job code A02
SELECT * FROM EMPLOYEE WHERE JOB_CODE = "A02";

--Select statement to show count of employees assigned to each job code
SELECT COUNT(EMP_ID) AS "TotalEmployees", JOB_CODE, JOB_DESCRIPTION FROM EMPLOYEE JOIN JOB USING (JOB_CODE) GROUP BY JOB_CODE;

--Select statement to show the earliest and most recent hire dates
SELECT MIN(HIRE_DATE) AS "EarliestHire", MAX(HIRE_DATE) AS "NewestHire" FROM EMPLOYEE;

--Select statement to show all job descriptions that include the word "Clerk"
SELECT JOB_DESCRIPTION FROM JOB GROUP BY JOB_CODE HAVING JOB_DESCRIPTION LIKE '%clerk%';

--Create a view called "EMP_VIEW" that shows EMP_ID, First/Last Name, and Job descriptions
CREATE VIEW EMP_VIEW AS
    SELECT EMP_ID, FIRST_NAME, LAST_NAME, JOB_DESCRIPTION FROM EMPLOYEE JOIN JOB USING (JOB_CODE);

SELECT * FROM EMP_VIEW;

--Save preceding steps to disk
COMMIT;