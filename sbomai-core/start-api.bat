@echo off
echo Starting SBOM AI Spring Boot API...
echo.

REM Set environment variables
set SPRING_PROFILES_ACTIVE=local
set DB_HOST=localhost
set DB_PORT=5432
set DB_NAME=sbomai
set DB_USERNAME=postgres
set DB_PASSWORD=password
set SBOMAI_UPLOAD_DIRECTORY=./uploads
set SBOMAI_PARSER_GO_EXECUTABLE=../sbomai-parser-go/sbomai-parser.exe

REM Create uploads directory if it doesn't exist
if not exist "uploads" mkdir uploads

REM Check if PostgreSQL is running
echo Checking PostgreSQL connection...
timeout /t 2 /nobreak >nul

REM Build the project
echo Building project...
call mvn clean install -DskipTests

if %ERRORLEVEL% neq 0 (
    echo Build failed! Please check the errors above.
    pause
    exit /b 1
)

echo.
echo Starting Spring Boot application...
echo API will be available at: http://localhost:8080/api/v1
echo Health check: http://localhost:8080/api/v1/actuator/health
echo.

REM Start the application
call mvn spring-boot:run

pause 