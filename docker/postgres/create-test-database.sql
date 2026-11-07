-- Runs once, when the database volume is created (see docker-compose.yml).
-- POSTGRES_DB creates the app database; this creates the one the tests use.
CREATE DATABASE career_copilot_test;
