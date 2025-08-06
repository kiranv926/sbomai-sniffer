@echo off
REM SBOMAI Database Initialization Script for Windows
REM This script sets up the PostgreSQL database for SBOMAI

setlocal enabledelayedexpansion

REM Configuration
set DB_NAME=sbomai_db
set DB_USER=sbomai_user
set DB_PASSWORD=sbomai_password
set DB_HOST=localhost
set DB_PORT=5432
set SCHEMA_FILE=schema\sbomai_schema.sql

echo === SBOMAI Database Initialization ===
echo Database: %DB_NAME%
echo User: %DB_USER%
echo Host: %DB_HOST%:%DB_PORT%
echo.

REM Check if PostgreSQL is running
pg_isready -h %DB_HOST% -p %DB_PORT% >nul 2>&1
if errorlevel 1 (
    echo Error: PostgreSQL is not running on %DB_HOST%:%DB_PORT%
    echo Please start PostgreSQL and try again.
    pause
    exit /b 1
)

REM Create database if it doesn't exist
echo Creating database '%DB_NAME%' if it doesn't exist...
createdb -h %DB_HOST% -p %DB_PORT% -U postgres %DB_NAME% >nul 2>&1 || echo Database already exists

REM Create user if it doesn't exist
echo Creating user '%DB_USER%' if it doesn't exist...
psql -h %DB_HOST% -p %DB_PORT% -U postgres -d %DB_NAME% -c "CREATE USER %DB_USER% WITH PASSWORD '%DB_PASSWORD%';" >nul 2>&1 || echo User already exists

REM Grant privileges
echo Granting privileges...
psql -h %DB_HOST% -p %DB_PORT% -U postgres -d %DB_NAME% -c "GRANT ALL PRIVILEGES ON DATABASE %DB_NAME% TO %DB_USER%;"
psql -h %DB_HOST% -p %DB_PORT% -U postgres -d %DB_NAME% -c "GRANT ALL PRIVILEGES ON SCHEMA public TO %DB_USER%;"

REM Apply schema
echo Applying database schema...
psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %DB_NAME% -f %SCHEMA_FILE%

REM Create initial data if exists
if exist "data\initial_data.sql" (
    echo Creating initial data...
    psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %DB_NAME% -f "data\initial_data.sql"
)

echo.
echo === Database initialization completed successfully! ===
echo Connection string: postgresql://%DB_USER%:%DB_PASSWORD%@%DB_HOST%:%DB_PORT%/%DB_NAME%
echo.
echo You can now connect to the database using:
echo psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %DB_NAME%
pause
