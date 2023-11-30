CREATE TABLE designations (
       id SERIAL PRIMARY KEY,
       title VARCHAR(100),
       leaves INTEGER
       );

CREATE TABLE employees(
       id SERIAL PRIMARY KEY,
       fname VARCHAR(50),
       lname VARCHAR(50),
       email VARCHAR(120),
       phone VARCHAR(50),
       rank INTEGER REFERENCES designations(id)
       );

CREATE TABLE leaves (
       id SERIAL PRIMARY KEY,
       date DATE,
       employee INTEGER REFERENCES employees(id),
       reason VARCHAR(200),
       UNIQUE (employee, date) -- An employee can take only one leave on a given day
       );

