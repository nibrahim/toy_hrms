CREATE TABLE employees(
       id SERIAL PRIMARY KEY,
       fname VARCHAR(50),
       lname VARCHAR(50),
       designation VARCHAR(100),
       email VARCHAR(120),
       phone VARCHAR(50)
       );

CREATE TABLE leaves (
       id SERIAL PRIMARY KEY,
       date DATE,
       employee INTEGER REFERENCES employees(id),
       reason VARCHAR(200),
       UNIQUE (employee, date) -- An employee can take only one leave on a given day
       );
