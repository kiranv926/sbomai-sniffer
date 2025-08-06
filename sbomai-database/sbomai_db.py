#!/usr/bin/env python3
"""
SBOMAI Database Connector
========================

This module provides a Python interface to the SBOMAI PostgreSQL database.
It handles all database operations for storing and retrieving SBOM data,
vulnerabilities, and analysis results.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
import psycopg2
from psycopg2.extras import RealDictCursor, Json
from psycopg2.pool import SimpleConnectionPool
import uuid

logger = logging.getLogger(__name__)


class SBOMAIDatabase:
    """Main database connector for SBOMAI"""
    
    def __init__(self, connection_string: str = None, **kwargs):
        """
        Initialize database connection
        
        Args:
            connection_string: PostgreSQL connection string
            **kwargs: Connection parameters (host, port, database, user, password)
        """
        if connection_string:
            self.connection_string = connection_string
        else:
            # Default connection parameters
            host = kwargs.get('host', 'localhost')
            port = kwargs.get('port', 5432)
            database = kwargs.get('database', 'sbomai_db')
            user = kwargs.get('user', 'sbomai_user')
            password = kwargs.get('password', 'sbomai_password')
            
            self.connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        
        # Initialize connection pool
        self.pool = SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            dsn=self.connection_string
        )
        
        logger.info("SBOMAI Database connector initialized")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
    
    def close(self):
        """Close all database connections"""
        if self.pool:
            self.pool.closeall()
            logger.info("Database connections closed")
    
    def get_connection(self):
        """Get a database connection from the pool"""
        return self.pool.getconn()
    
    def return_connection(self, conn):
        """Return a connection to the pool"""
        self.pool.putconn(conn)
    
    def execute_query(self, query: str, params: tuple = None, fetch: bool = True):
        """Execute a database query"""
        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                if fetch:
                    return cursor.fetchall()
                else:
                    conn.commit()
                    return cursor.rowcount
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Database query failed: {e}")
            raise
        finally:
            if conn:
                self.return_connection(conn)
    
    def create_scan(self, target_identifier: str, scan_type: str) -> str:
        """Create a new scan record"""
        scan_id = str(uuid.uuid4())
        query = """
        INSERT INTO scans (id, target_identifier, scan_type, status)
        VALUES (%s, %s, %s, 'PENDING')
        RETURNING id
        """
        self.execute_query(query, (scan_id, target_identifier, scan_type), fetch=False)
        logger.info(f"Created scan {scan_id} for {target_identifier}")
        return scan_id
    
    def update_scan_status(self, scan_id: str, status: str, **kwargs):
        """Update scan status and metadata"""
        query = """
        UPDATE scans 
        SET status = %s, 
            completed_at = CASE WHEN %s IN ('COMPLETED', 'FAILED') THEN NOW() ELSE completed_at END,
            components_found = %s,
            vulnerabilities_found = %s,
            risk_score = %s,
            error_message = %s,
            updated_at = NOW()
        WHERE id = %s
        """
        
        components_found = kwargs.get('components_found', 0)
        vulnerabilities_found = kwargs.get('vulnerabilities_found', 0)
        risk_score = kwargs.get('risk_score', 0.0)
        error_message = kwargs.get('error_message')
        
        self.execute_query(query, (
            status, status, components_found, vulnerabilities_found, 
            risk_score, error_message, scan_id
        ), fetch=False)
        
        logger.info(f"Updated scan {scan_id} status to {status}")
    
    def store_sbom_document(self, scan_id: str, sbom_data: Dict[str, Any], 
                           format_type: str = 'cyclonedx') -> str:
        """Store SBOM document in the database"""
        sbom_id = str(uuid.uuid4())
        query = """
        INSERT INTO sbom_documents (id, scan_id, format, spec_version, raw_json)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
        """
        
        spec_version = sbom_data.get('specVersion', '1.0')
        
        self.execute_query(query, (
            sbom_id, scan_id, format_type, spec_version, Json(sbom_data)
        ), fetch=False)
        
        logger.info(f"Stored SBOM document {sbom_id} for scan {scan_id}")
        return sbom_id
    
    def store_components(self, sbom_id: str, components: List[Dict[str, Any]]):
        """Store SBOM components in normalized tables"""
        for component in components:
            component_id = str(uuid.uuid4())
            query = """
            INSERT INTO sbom_components (
                id, sbom_id, bom_ref, name, version, type, purl, cpe, 
                license_id, description, author, supplier, checksums, properties
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            # Extract component data
            bom_ref = component.get('bom-ref', component.get('id', ''))
            name = component.get('name', '')
            version = component.get('version', '')
            component_type = component.get('type', 'library')
            purl = component.get('purl', '')
            cpe = component.get('cpe', '')
            
            # Handle licenses
            licenses = component.get('licenses', [])
            license_id = licenses[0].get('license', {}).get('id', '') if licenses else ''
            
            # Handle checksums
            checksums = component.get('hashes', [])
            checksums_json = {h.get('alg', ''): h.get('content', '') for h in checksums}
            
            # Handle properties
            properties = component.get('properties', [])
            properties_json = {p.get('name', ''): p.get('value', '') for p in properties}
            
            self.execute_query(query, (
                component_id, sbom_id, bom_ref, name, version, component_type,
                purl, cpe, license_id, component.get('description', ''),
                component.get('author', ''), component.get('supplier', ''),
                Json(checksums_json), Json(properties_json)
            ), fetch=False)
        
        logger.info(f"Stored {len(components)} components for SBOM {sbom_id}")
    
    def store_vulnerabilities(self, vulnerabilities: List[Dict[str, Any]]):
        """Store vulnerability data"""
        for vuln in vulnerabilities:
            query = """
            INSERT INTO vulnerabilities (
                cve_id, description, severity, cvss_score, cvss_vector,
                published_at, source_name, source_url, references
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (cve_id) DO UPDATE SET
                description = EXCLUDED.description,
                severity = EXCLUDED.severity,
                cvss_score = EXCLUDED.cvss_score,
                cvss_vector = EXCLUDED.cvss_vector,
                updated_at = NOW()
            """
            
            self.execute_query(query, (
                vuln.get('id', ''),
                vuln.get('description', ''),
                vuln.get('severity', 'UNKNOWN'),
                vuln.get('cvss_score'),
                vuln.get('cvss_vector', ''),
                vuln.get('published_at'),
                vuln.get('source', 'NVD'),
                vuln.get('source_url', ''),
                Json(vuln.get('references', []))
            ), fetch=False)
        
        logger.info(f"Stored {len(vulnerabilities)} vulnerabilities")
    
    def link_component_vulnerabilities(self, component_id: str, vulnerability_ids: List[str]):
        """Link components to vulnerabilities"""
        for vuln_id in vulnerability_ids:
            query = """
            INSERT INTO component_vulnerabilities (
                sbom_component_id, vulnerability_id, risk_score, exploit_probability
            ) VALUES (%s, %s, %s, %s)
            ON CONFLICT (sbom_component_id, vulnerability_id) DO UPDATE SET
                risk_score = EXCLUDED.risk_score,
                exploit_probability = EXCLUDED.exploit_probability,
                updated_at = NOW()
            """
            
            # Mock risk scores (replace with real AI analysis)
            risk_score = 0.5
            exploit_probability = 0.3
            
            self.execute_query(query, (
                component_id, vuln_id, risk_score, exploit_probability
            ), fetch=False)
        
        logger.info(f"Linked {len(vulnerability_ids)} vulnerabilities to component {component_id}")
    
    def get_scan_summary(self, scan_id: str) -> Dict[str, Any]:
        """Get comprehensive scan summary"""
        query = """
        SELECT 
            s.*,
            sd.format as sbom_format,
            sd.spec_version as sbom_spec_version,
            COUNT(sc.id) as total_components,
            COUNT(cv.id) as total_vulnerabilities
        FROM scans s
        LEFT JOIN sbom_documents sd ON s.id = sd.scan_id
        LEFT JOIN sbom_components sc ON sd.id = sc.sbom_id
        LEFT JOIN component_vulnerabilities cv ON sc.id = cv.sbom_component_id
        WHERE s.id = %s
        GROUP BY s.id, sd.format, sd.spec_version
        """
        
        result = self.execute_query(query, (scan_id,))
        return dict(result[0]) if result else {}
    
    def get_vulnerability_stats(self) -> Dict[str, Any]:
        """Get vulnerability statistics"""
        query = "SELECT * FROM get_vulnerability_stats()"
        result = self.execute_query(query)
        return dict(result[0]) if result else {}
    
    def search_components(self, search_term: str) -> List[Dict[str, Any]]:
        """Search components by name or PURL"""
        query = "SELECT * FROM search_components(%s)"
        result = self.execute_query(query, (search_term,))
        return [dict(row) for row in result]
    
    def get_recent_scans(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent scans"""
        query = """
        SELECT * FROM scan_summary 
        ORDER BY initiated_at DESC 
        LIMIT %s
        """
        result = self.execute_query(query, (limit,))
        return [dict(row) for row in result]
    
    def store_ai_analysis(self, scan_id: str, analysis_type: str, 
                         results: Dict[str, Any], model_version: str = "1.0"):
        """Store AI analysis results"""
        analysis_id = str(uuid.uuid4())
        query = """
        INSERT INTO ai_analysis_results (
            id, scan_id, analysis_type, model_version, results, confidence_score
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        confidence_score = results.get('confidence_score', 0.8)
        
        self.execute_query(query, (
            analysis_id, scan_id, analysis_type, model_version,
            Json(results), confidence_score
        ), fetch=False)
        
        logger.info(f"Stored AI analysis {analysis_id} for scan {scan_id}")
    
    def store_risk_assessment(self, scan_id: str, risk_score: float,
                             risk_factors: Dict[str, Any], recommendations: List[str]):
        """Store risk assessment results"""
        assessment_id = str(uuid.uuid4())
        query = """
        INSERT INTO risk_assessments (
            id, scan_id, overall_risk_score, risk_factors, recommendations
        ) VALUES (%s, %s, %s, %s, %s)
        """
        
        self.execute_query(query, (
            assessment_id, scan_id, risk_score,
            Json(risk_factors), Json(recommendations)
        ), fetch=False)
        
        logger.info(f"Stored risk assessment {assessment_id} for scan {scan_id}")


# Convenience function for quick database operations
def get_db_connection(connection_string: str = None, **kwargs) -> SBOMAIDatabase:
    """Get a database connection with default settings"""
    if connection_string:
        return SBOMAIDatabase(connection_string)
    else:
        return SBOMAIDatabase(**kwargs)


# Example usage
if __name__ == "__main__":
    # Example: Connect to database and perform operations
    with get_db_connection() as db:
        # Get vulnerability statistics
        stats = db.get_vulnerability_stats()
        print(f"Vulnerability stats: {stats}")
        
        # Get recent scans
        recent_scans = db.get_recent_scans(5)
        print(f"Recent scans: {recent_scans}")
