create user bookcrossing_admin password 'simplepass';

create database bookcrossing_db encoding 'utf-8';
grant all privileges on database bookcrossing_db to bookcrossing_admin;
alter database bookcrossing_db owner to bookcrossing_admin;

create database bookcrossing_test_db encoding 'utf-8';
grant all privileges on database bookcrossing_test_db to bookcrossing_admin;
alter database bookcrossing_test_db owner to bookcrossing_admin;
