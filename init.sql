-- Create the user
CREATE USER wedding_user WITH PASSWORD 'wedding_password' LOGIN;

-- Create the database
CREATE DATABASE wedding_db;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE wedding_db TO wedding_user;

-- Connect to the wedding_db
\c wedding_db

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO wedding_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO wedding_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO wedding_user; 