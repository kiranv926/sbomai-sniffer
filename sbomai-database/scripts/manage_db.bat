@echo off
REM SBOMAI Database Docker Management Script for Windows
REM This script provides easy management of the PostgreSQL database in Docker

setlocal enabledelayedexpansion

REM Configuration
set COMPOSE_FILE=docker-compose.yml
set DB_NAME=sbomai_db
set DB_USER=sbomai_user
set DB_PASSWORD=sbomai_password
set DB_HOST=localhost
set DB_PORT=5432

REM Colors for output (Windows doesn't support ANSI colors, so we'll use text)
set INFO=[INFO]
set SUCCESS=[SUCCESS]
set WARNING=[WARNING]
set ERROR=[ERROR]

REM Function to print status
:print_status
echo %INFO% %~1
goto :eof

REM Function to print success
:print_success
echo %SUCCESS% %~1
goto :eof

REM Function to print warning
:print_warning
echo %WARNING% %~1
goto :eof

REM Function to print error
:print_error
echo %ERROR% %~1
goto :eof

REM Function to check if Docker is running
:check_docker
docker info >nul 2>&1
if errorlevel 1 (
    call :print_error "Docker is not running. Please start Docker Desktop and try again."
    pause
    exit /b 1
)
goto :eof

REM Function to start the database
:start_db
call :print_status "Starting SBOMAI PostgreSQL database..."
call :check_docker

docker-compose -f %COMPOSE_FILE% up -d postgres

call :print_status "Waiting for database to be ready..."
timeout /t 10 /nobreak >nul

REM Wait for database to be healthy
set timeout=30
:wait_loop
docker-compose -f %COMPOSE_FILE% exec -T postgres pg_isready -U %DB_USER% -d %DB_NAME% >nul 2>&1
if not errorlevel 1 (
    call :print_success "Database is ready!"
    goto :start_success
)
timeout /t 2 /nobreak >nul
set /a timeout-=1
if %timeout% leq 0 (
    call :print_error "Database failed to start within 60 seconds"
    pause
    exit /b 1
)
goto :wait_loop

:start_success
call :print_success "PostgreSQL database started successfully!"
call :print_status "Connection details:"
echo   Host: %DB_HOST%
echo   Port: %DB_PORT%
echo   Database: %DB_NAME%
echo   Username: %DB_USER%
echo   Password: %DB_PASSWORD%
echo   Connection string: postgresql://%DB_USER%:%DB_PASSWORD%@%DB_HOST%:%DB_PORT%/%DB_NAME%
goto :eof

REM Function to stop the database
:stop_db
call :print_status "Stopping SBOMAI PostgreSQL database..."
docker-compose -f %COMPOSE_FILE% down
call :print_success "Database stopped successfully!"
goto :eof

REM Function to restart the database
:restart_db
call :print_status "Restarting SBOMAI PostgreSQL database..."
call :stop_db
call :start_db
goto :eof

REM Function to show database status
:status_db
call :print_status "Checking database status..."

docker-compose -f %COMPOSE_FILE% ps | findstr "Up" >nul
if not errorlevel 1 (
    call :print_success "Database is running"
    docker-compose -f %COMPOSE_FILE% ps
) else (
    call :print_warning "Database is not running"
)
goto :eof

REM Function to connect to database
:connect_db
call :print_status "Connecting to database..."
docker-compose -f %COMPOSE_FILE% exec postgres psql -U %DB_USER% -d %DB_NAME%
goto :eof

REM Function to run SQL script
:run_sql
if "%~1"=="" (
    call :print_error "Please provide a SQL file path"
    pause
    exit /b 1
)

call :print_status "Running SQL script: %~1"
docker-compose -f %COMPOSE_FILE% exec -T postgres psql -U %DB_USER% -d %DB_NAME% -f "/opt/data/%~1"
goto :eof

REM Function to backup database
:backup_db
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "backup_file=backup_%YYYY%%MM%%DD%_%HH%%Min%%Sec%.sql"

call :print_status "Creating database backup: %backup_file%"

if not exist "backups" mkdir backups
docker-compose -f %COMPOSE_FILE% exec -T postgres pg_dump -U %DB_USER% -d %DB_NAME% > "backups\%backup_file%"
call :print_success "Backup created: backups\%backup_file%"
goto :eof

REM Function to show logs
:show_logs
call :print_status "Showing database logs..."
docker-compose -f %COMPOSE_FILE% logs -f postgres
goto :eof

REM Function to reset database
:reset_db
call :print_warning "This will delete all data and recreate the database. Are you sure? (y/N)"
set /p response=
if /i "!response!"=="y" (
    call :print_status "Resetting database..."
    docker-compose -f %COMPOSE_FILE% down -v
    docker-compose -f %COMPOSE_FILE% up -d postgres
    call :print_success "Database reset successfully!"
) else (
    call :print_status "Database reset cancelled"
)
goto :eof

REM Function to show help
:show_help
echo SBOMAI Database Management Script
echo.
echo Usage: %0 [COMMAND]
echo.
echo Commands:
echo   start       Start the PostgreSQL database
echo   stop        Stop the PostgreSQL database
echo   restart     Restart the PostgreSQL database
echo   status      Show database status
echo   connect     Connect to the database (interactive)
echo   run-sql     Run a SQL script (provide file path)
echo   backup      Create a database backup
echo   logs        Show database logs
echo   reset       Reset database (delete all data)
echo   help        Show this help message
echo.
echo Examples:
echo   %0 start
echo   %0 run-sql my_script.sql
echo   %0 backup
goto :eof

REM Main script logic
if "%1"=="" goto :show_help

if "%1"=="start" goto :start_db
if "%1"=="stop" goto :stop_db
if "%1"=="restart" goto :restart_db
if "%1"=="status" goto :status_db
if "%1"=="connect" goto :connect_db
if "%1"=="run-sql" goto :run_sql
if "%1"=="backup" goto :backup_db
if "%1"=="logs" goto :show_logs
if "%1"=="reset" goto :reset_db
if "%1"=="help" goto :show_help

call :print_error "Unknown command: %1"
call :show_help
pause
exit /b 1
