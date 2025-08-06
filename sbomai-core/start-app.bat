@echo off
echo Starting SBOMAI Core Orchestrator...
echo.

echo Building the application...
call mvn clean package -DskipTests

if %ERRORLEVEL% NEQ 0 (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo Starting the application...
java -jar target/sbomai-core-1.0.0-SNAPSHOT.jar --spring.profiles.active=test

pause
