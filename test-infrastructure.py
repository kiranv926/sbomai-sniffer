#!/usr/bin/env python3
"""
Test script to verify SBOMAI infrastructure connectivity
"""

import requests
import psycopg2
import json
from kafka import KafkaProducer, KafkaConsumer
import time

def test_postgres():
    """Test PostgreSQL connectivity"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="sbomai_db",
            user="sbomai_user",
            password="sbomai_password"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        cursor.close()
        conn.close()
        print("✅ PostgreSQL: Connected successfully")
        print(f"   Version: {version[0]}")
        return True
    except Exception as e:
        print(f"❌ PostgreSQL: Connection failed - {e}")
        return False

def test_kafka():
    """Test Kafka connectivity"""
    try:
        # Test producer
        producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        
        # Send a test message
        test_message = {"test": "SBOMAI infrastructure test", "timestamp": time.time()}
        producer.send('test-topic', test_message)
        producer.flush()
        producer.close()
        
        print("✅ Kafka: Producer test successful")
        
        # Test consumer
        consumer = KafkaConsumer(
            'test-topic',
            bootstrap_servers=['localhost:9092'],
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='earliest',
            group_id='test-group'
        )
        
        # Wait for message
        for message in consumer:
            print(f"✅ Kafka: Consumer test successful - Received: {message.value}")
            break
        
        consumer.close()
        return True
        
    except Exception as e:
        print(f"❌ Kafka: Connection failed - {e}")
        return False

def test_kafka_ui():
    """Test Kafka UI accessibility"""
    try:
        response = requests.get("http://localhost:8080", timeout=5)
        if response.status_code == 200:
            print("✅ Kafka UI: Accessible at http://localhost:8080")
            return True
        else:
            print(f"❌ Kafka UI: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Kafka UI: Connection failed - {e}")
        return False

def test_pgadmin():
    """Test pgAdmin accessibility"""
    try:
        response = requests.get("http://localhost:8082", timeout=5)
        if response.status_code == 200:
            print("✅ pgAdmin: Accessible at http://localhost:8082")
            print("   Login: admin@sbomai.com / admin123")
            return True
        else:
            print(f"❌ pgAdmin: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ pgAdmin: Connection failed - {e}")
        return False

def main():
    """Run all infrastructure tests"""
    print("🚀 Testing SBOMAI Infrastructure...")
    print("=" * 50)
    
    tests = [
        ("PostgreSQL", test_postgres),
        ("Kafka", test_kafka),
        ("Kafka UI", test_kafka_ui),
        ("pgAdmin", test_pgadmin)
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n🔍 Testing {name}...")
        result = test_func()
        results.append((name, result))
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print("=" * 50)
    
    passed = 0
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:12} {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Summary: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All infrastructure components are working!")
        print("\n📋 Next Steps:")
        print("1. Access Kafka UI: http://localhost:8080")
        print("2. Access pgAdmin: http://localhost:8082")
        print("3. Build and run the Java core application")
        print("4. Test the Go parser")
        print("5. Integrate with Python AI engine")
    else:
        print("⚠️  Some components need attention. Check Docker logs.")

if __name__ == "__main__":
    main() 