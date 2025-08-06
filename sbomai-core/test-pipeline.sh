#!/bin/bash
# SBOMAI Core Test Script
# This script demonstrates the complete SBOM processing pipeline

echo "=== SBOMAI Core Orchestrator Test ==="
echo ""

# Test 1: Health Check
echo "1. Testing Health Check..."
curl -s http://localhost:8080/api/v1/orchestration/health
echo ""
echo ""

# Test 2: Trigger SBOM Processing
echo "2. Triggering SBOM Processing..."
SCAN_ID=
echo "Generated Scan ID: "
echo ""

# Sample SBOM content (CycloneDX format)
SAMPLE_SBOM='{
  "bomFormat": "CycloneDX",
  "specVersion": "1.6",
  "metadata": {
    "timestamp": "2025-08-05T12:00:00Z",
    "tools": [
      {
        "vendor": "SBOMAI",
        "name": "sbomai-parser",
        "version": "1.0.0"
      }
    ]
  },
  "components": [
    {
      "bom-ref": "pkg:maven/org.apache.logging.log4j/log4j-core@2.14.1",
      "name": "log4j-core",
      "version": "2.14.1",
      "type": "library",
      "purl": "pkg:maven/org.apache.logging.log4j/log4j-core@2.14.1",
      "licenses": [
        {
          "license": {
            "id": "Apache-2.0"
          }
        }
      ]
    },
    {
      "bom-ref": "pkg:maven/com.google.guava/guava@30.0-jre",
      "name": "guava",
      "version": "30.0-jre",
      "type": "library",
      "purl": "pkg:maven/com.google.guava/guava@30.0-jre",
      "licenses": [
        {
          "license": {
            "id": "Apache-2.0"
          }
        }
      ]
    }
  ]
}'

# Create test event
TEST_EVENT='{
  "scanId": "''",
  "rawSbomContent": "''",
  "targetIdentifier": "test-project",
  "scanType": "repository"
}'

echo "Sending test event..."
curl -X POST http://localhost:8080/api/v1/orchestration/trigger-sbom-processing \
  -H "Content-Type: application/json" \
  -d ""
echo ""
echo ""

# Test 3: Check Database
echo "3. Checking Database..."
echo "Connecting to PostgreSQL..."
docker exec sbomai-postgres psql -U sbomai_user -d sbomai_db -c "SELECT id, target_identifier, status, created_at FROM scans ORDER BY created_at DESC LIMIT 5;"
echo ""

# Test 4: Check Kafka Topics
echo "4. Checking Kafka Topics..."
echo "Available topics:"
docker exec sbomai-kafka kafka-topics --bootstrap-server localhost:9092 --list
echo ""

echo "=== Test Completed ==="
echo ""
echo "Next Steps:"
echo "1. Check Kafka UI: http://localhost:8081"
echo "2. Check pgAdmin: http://localhost:8082"
echo "3. Monitor application logs: docker logs sbomai-core"
echo ""
