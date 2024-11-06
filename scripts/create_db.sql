-- reset database --
DROP DATABASE :db;
CREATE DATABASE :db;
\c :db;

-- clean data --
DROP TABLE IF EXISTS employee CASCADE;
DROP TABLE IF EXISTS employee_team CASCADE;
DROP TABLE IF EXISTS employee_vacation CASCADE;
DROP TYPE IF EXISTS VacationType;

-- employee --
CREATE TABLE employee
(
    id integer primary key generated always as identity,
	team_id INTEGER,
	email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255)
);

-- employee team --
CREATE TABLE employee_team
(
    id integer primary key generated always as identity,
	name VARCHAR(255) NOT NULL UNIQUE
);

ALTER TABLE employee ADD CONSTRAINT FK_employee_team_id FOREIGN KEY (team_id) REFERENCES employee(id);

-- employee vacation --
CREATE TYPE VacationType AS ENUM ('Unpaid leave', 'Paid leave');
CREATE TABLE employee_vacation
(
    id integer primary key generated always as identity,
	user_id integer NOT NULL,
    vacation_type VacationType,
    start_date DATE,
	end_date DATE
);

ALTER TABLE employee_vacation ADD CONSTRAINT FK_employee_vacation_user_id FOREIGN KEY (user_id) REFERENCES employee(id);

