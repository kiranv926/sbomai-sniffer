#!/bin/bash

echo "Starting SBOM AI Spring Boot API..."
echo

# Set environment variables
export SPRING_PROFILES_ACTIVE=local
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=sbomai
export DB_USERNAME=postgres
export DB_PASSWORD=password
export SBOMAI_UPLOAD_DIRECTORY=./uploads
export SBOMAI_PARSER_GO_EXECUTABLE=../sbomai-parser-go/sbomai-parser.exe

# Create uploads directory if it doesn't exist
mkdir -p uploads

# Check if PostgreSQL is running
echo "Checking PostgreSQL connection..."
if ! pg_isready -h localhost -p 5432 -U postgres > /dev/null 2>&1; then
    echo "Warning: PostgreSQL is not running or not accessible"
    echo "Please start PostgreSQL before running the API"
    echo
fi

# Build the project
echo "Building project..."
if ! mvn clean install -DskipTests; then
    echo "Build failed! Please check the errors above."
    exit 1
fi

echo
echo "Starting Spring Boot application..."
echo "API will be available at: http://localhost:8080/api/v1"
echo "Health check: http://localhost:8080/api/v1/actuator/health"
echo

# Start the application
mvn spring-boot:run 