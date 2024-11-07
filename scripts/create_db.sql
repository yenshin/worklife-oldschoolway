-- reset database --
DROP DATABASE :db;
CREATE DATABASE :db;
\c :db;

-- clean data --
DROP TABLE IF EXISTS employee CASCADE;
DROP TABLE IF EXISTS employee_team CASCADE;
DROP TABLE IF EXISTS employee_vacation CASCADE;
DROP TABLE IF EXISTS logs CASCADE;
DROP TYPE IF EXISTS LogType;
DROP TYPE IF EXISTS VacationType;

-- employee --
CREATE TABLE employee
(
    internal_id integer primary key generated always as identity,
	external_id UUID NOT NULL UNIQUE,	
	email VARCHAR(255) NOT NULL UNIQUE,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
	team_id INTEGER DEFAULT NULL
);

CREATE INDEX idx_employee_internal_id ON employee (internal_id);
CREATE INDEX idx_employee_external_id ON employee (external_id);
CREATE INDEX idx_email ON employee (email);
CREATE INDEX idx_team_id ON employee (team_id);

-- employee team --
CREATE TABLE employee_team
(
    internal_id integer primary key generated always as identity,
	external_id UUID NOT NULL UNIQUE,
	team_name VARCHAR(255) NOT NULL UNIQUE
);
CREATE INDEX idx_employee_team_internal_id ON employee_team (internal_id);
CREATE INDEX idx_employee_team_external_id ON employee_team (external_id);
CREATE INDEX idx_team_name ON employee_team (team_name);

ALTER TABLE employee ADD CONSTRAINT FK_employee_team_id FOREIGN KEY (team_id) REFERENCES employee_team(internal_id);

-- employee vacation --
CREATE TYPE vacationtype AS ENUM ('UnpaidLeave', 'PaidLeave');
CREATE TABLE employee_vacation
(
    internal_id integer primary key generated always as identity,
	external_id UUID NOT NULL UNIQUE,
	user_id integer NOT NULL,
    vacation_type vacationtype,
    start_date DATE,
	end_date DATE
);

CREATE INDEX idx_employee_vacation_internal_id ON employee_vacation (internal_id);
CREATE INDEX idx_employee_vacation_external_id ON employee_vacation (external_id);
CREATE INDEX idx_evfk_user_id ON employee_vacation (user_id);
CREATE INDEX idx_vacation_type ON employee_vacation (vacation_type);
CREATE INDEX idx_start_date ON employee_vacation (start_date);
CREATE INDEX idx_end_date ON employee_vacation (end_date);

ALTER TABLE employee_vacation ADD CONSTRAINT FK_employee_vacation_user_id FOREIGN KEY (user_id) REFERENCES employee(internal_id);

-- logs --
CREATE TYPE logtype AS ENUM ('DEBUG', 'INFO', 'WARNING', 'ERROR');
CREATE TABLE logs
(
    internal_id integer primary key generated always as identity,
	external_id UUID NOT NULL UNIQUE,
	log_type logtype NOT NULL,
    prefix TEXT,
    msg TEXT,
	additionnal_info TEXT
);
CREATE INDEX idx_log_internal_id ON logs (internal_id);
CREATE INDEX idx_log_external_id ON logs (external_id);
CREATE INDEX idx_log_log_type ON logs (log_type);