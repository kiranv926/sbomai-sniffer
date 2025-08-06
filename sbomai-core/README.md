# SBOMAI Core Orchestrator
# =======================

## Overview

SBOMAI Core is the central orchestration service that manages the complete SBOM processing pipeline from raw ingestion to vulnerability analysis. It coordinates between different microservices and ensures data consistency across the entire system.

## Architecture

`
        
   Kafka Topics        PostgreSQL DB        Microservices  
                                                           
 sbom.received      scans              Go Parser       
 sbom.processed       sbom_documents       Python Engine   
 vuln.detected        sbom_components                      
 scan.completed       vulnerabilities                      
 scan.failed          component_vulns                      
        
                              
                              
                    
                      SBOMAI Core    
                     Orchestrator    
                                     
                      Kafka Listener
                      HTTP Client   
                      JPA Repos     
                      Event Publisher
                    
`

## Features

- **Event-Driven Architecture**: Uses Apache Kafka for reliable message processing
- **Microservice Integration**: Coordinates with Go parser and Python analysis services
- **Database Management**: Stores and manages SBOM data in PostgreSQL
- **Error Handling**: Comprehensive error handling with retry mechanisms
- **Monitoring**: Health checks and metrics via Spring Actuator
- **Scalability**: Concurrent message processing and connection pooling

## Technology Stack

- **Java 17** with Spring Boot 3.x
- **Spring Kafka** for message queue integration
- **Spring Data JPA** for database operations
- **WebClient** for HTTP communication
- **PostgreSQL** with JSONB support
- **Apache Kafka** for event streaming
- **Docker** for containerization

## Quick Start

### 1. Prerequisites

- Docker and Docker Compose
- Java 17+
- Maven 3.6+

### 2. Start the Infrastructure

`ash
# Start PostgreSQL, Kafka, and supporting services
docker-compose up -d postgres kafka zookeeper kafka-ui pgadmin
`

### 3. Build and Run

`ash
# Build the application
mvn clean package

# Run the application
java -jar target/sbomai-core-1.0.0-SNAPSHOT.jar
`

### 4. Access Services

- **SBOMAI Core**: http://localhost:8080
- **Kafka UI**: http://localhost:8081
- **pgAdmin**: http://localhost:8082 (admin@sbomai.local / admin123)
- **PostgreSQL**: localhost:5432

## API Endpoints

### Health Check
`
GET /api/v1/orchestration/health
`

### Trigger SBOM Processing (Testing)
`
POST /api/v1/orchestration/trigger-sbom-processing
Content-Type: application/json

{
  "scanId": "550e8400-e29b-41d4-a716-446655440000",
  "rawSbomContent": "{...}",
  "targetIdentifier": "alpine:latest",
  "scanType": "docker_image"
}
`

## Kafka Topics

- sbom.received - Incoming SBOM processing requests
- sbom.processed - SBOM parsing completed
- ulnerabilities.detected - Vulnerability analysis results
- scan.completed - Scan processing completed
- scan.failed - Scan processing failed

## Configuration

### Application Properties

`yaml
# Database
spring.datasource.url: jdbc:postgresql://localhost:5432/sbomai_db
spring.datasource.username: sbomai_user
spring.datasource.password: sbomai_password

# Kafka
spring.kafka.bootstrap-servers: localhost:9092
spring.kafka.consumer.group-id: sbomai-core

# Microservices
sbomai.parser.url: http://localhost:8081
sbomai.analysis.url: http://localhost:8082
`

## Processing Pipeline

### 1. SBOM Received Event
- Consumes sbom.received message
- Updates scan status to PARSING
- Calls Go parser service
- Saves raw SBOM to database
- Extracts and stores components
- Publishes sbom.processed event
- Triggers vulnerability analysis

### 2. Vulnerability Analysis
- Receives analysis results via ulnerabilities.detected
- Saves vulnerabilities to database
- Links vulnerabilities to components
- Updates scan status to COMPLETED
- Publishes scan.completed event

### 3. Error Handling
- Comprehensive retry mechanisms
- Dead letter queue for failed messages
- Detailed error logging
- Status tracking for all operations

## Development

### Building from Source

`ash
git clone <repository>
cd sbomai-core
mvn clean install
`

### Running Tests

`ash
mvn test
`

### Local Development

`ash
# Start dependencies
docker-compose up -d postgres kafka

# Run application
mvn spring-boot:run
`

## Monitoring

### Health Checks
- Application health: /actuator/health
- Database connectivity
- Kafka connectivity
- Microservice connectivity

### Metrics
- Prometheus metrics: /actuator/prometheus
- Custom business metrics
- Performance monitoring

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check PostgreSQL is running
   - Verify connection credentials
   - Check network connectivity

2. **Kafka Connection Failed**
   - Ensure Kafka and Zookeeper are running
   - Check bootstrap servers configuration
   - Verify topic creation

3. **Microservice Communication Failed**
   - Check service URLs
   - Verify service availability
   - Check network connectivity

### Logs

`ash
# View application logs
docker logs sbomai-core

# View Kafka logs
docker logs sbomai-kafka

# View database logs
docker logs sbomai-postgres
`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
