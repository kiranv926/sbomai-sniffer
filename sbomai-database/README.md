# SBOMAI Database Project
# ======================

This directory contains the PostgreSQL database setup for SBOMAI.

## Quick Start

### 1. Start the Database
`ash
# Windows
scripts\manage_db.bat start

# Linux/Mac
scripts/manage_db.sh start
`

### 2. Access pgAdmin (Web Interface)
- URL: http://localhost:8080
- Email: admin@sbomai.local
- Password: admin123

### 3. Connect via Command Line
`ash
# Using the management script
scripts\manage_db.bat connect

# Direct connection
psql -h localhost -p 5432 -U sbomai_user -d sbomai_db
`

## Project Structure

`
sbomai-database/
 schema/
    sbomai_schema.sql          # Main database schema
 migrations/                     # Database migrations
 scripts/
    manage_db.bat              # Windows management script
    manage_db.sh               # Linux/Mac management script
    init_database.bat          # Database initialization
 data/
    initial_data.sql           # Sample data and functions
 docker-compose.yml             # Docker configuration
 sbomai_db.py                   # Python database connector
 requirements.txt               # Python dependencies
`

## Database Schema

### Core Tables
- **scans**: Scan metadata and status
- **sbom_documents**: Raw SBOM JSON documents
- **sbom_components**: Normalized component data
- **vulnerabilities**: Vulnerability information
- **component_vulnerabilities**: Component-vulnerability relationships
- **knowledge_base_docs**: RAG knowledge base
- **ai_analysis_results**: AI/ML analysis results
- **risk_assessments**: Risk assessment data
- **audit_logs**: System audit trail

### Key Features
- JSONB storage for flexible SBOM data
- Full-text search capabilities
- Optimized indexes for performance
- Audit logging
- AI analysis result storage
- Risk assessment tracking

## Usage Examples

### Python Integration
`python
from sbomai_db import get_db_connection

# Connect to database
with get_db_connection() as db:
    # Create a new scan
    scan_id = db.create_scan("alpine:latest", "docker_image")
    
    # Store SBOM data
    sbom_id = db.store_sbom_document(scan_id, sbom_data)
    
    # Get scan summary
    summary = db.get_scan_summary(scan_id)
    print(summary)
`

### Database Management
`ash
# Start database
scripts\manage_db.bat start

# Check status
scripts\manage_db.bat status

# Create backup
scripts\manage_db.bat backup

# View logs
scripts\manage_db.bat logs

# Stop database
scripts\manage_db.bat stop
`

## Configuration

### Environment Variables
- DB_NAME: Database name (default: sbomai_db)
- DB_USER: Database user (default: sbomai_user)
- DB_PASSWORD: Database password (default: sbomai_password)
- DB_HOST: Database host (default: localhost)
- DB_PORT: Database port (default: 5432)

### Docker Configuration
The database runs in Docker containers:
- **PostgreSQL 15**: Main database
- **pgAdmin 4**: Web-based administration interface

## Security Notes
- Default passwords are used for development
- Change passwords for production deployment
- Consider using Docker secrets for sensitive data
- Enable SSL/TLS for production connections

## Performance Optimization
- JSONB indexes for SBOM data queries
- Full-text search indexes
- Connection pooling in Python connector
- Optimized table structure for common queries
