-- Initial data for SBOMAI database
-- This script populates the database with sample data and configurations

-- Insert sample vulnerabilities for testing
INSERT INTO vulnerabilities (cve_id, description, severity, cvss_score, cvss_vector, published_at, source_name) VALUES
('CVE-2021-44228', 'Apache Log4j2 JNDI features do not protect against attacker controlled LDAP and other JNDI related endpoints', 'CRITICAL', 10.0, 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H', '2021-12-10', 'NVD'),
('CVE-2021-45046', 'Apache Log4j2 Thread Context Lookup Pattern vulnerable to denial of service', 'HIGH', 9.0, 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H', '2021-12-14', 'NVD'),
('CVE-2022-22965', 'Spring Framework RCE via Data Binding on JDK 9+', 'CRITICAL', 9.8, 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H', '2022-03-31', 'NVD'),
('CVE-2022-22963', 'Spring Cloud Function SpEL Injection leading to Remote Code Execution', 'CRITICAL', 9.8, 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H', '2022-03-29', 'NVD'),
('CVE-2023-24998', 'Apache Commons Text vulnerable to remote code execution', 'CRITICAL', 9.8, 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H', '2023-03-21', 'NVD')
ON CONFLICT (cve_id) DO NOTHING;

-- Insert sample knowledge base documents
INSERT INTO knowledge_base_docs (title, content, content_type, tags) VALUES
('Log4j Remediation Guide', 'To remediate Log4j vulnerabilities, update to version 2.17.1 or later. For immediate mitigation, set system property log4j2.formatMsgNoLookups=true or remove JndiLookup class from classpath.', 'remediation_guide', ARRAY['log4j', 'remediation', 'java']),
('Spring Framework Security Best Practices', 'Always validate and sanitize user inputs, use latest Spring Framework versions, enable security headers, and implement proper authentication and authorization.', 'security_policy', ARRAY['spring', 'security', 'java']),
('Dependency Management Guidelines', 'Regularly update dependencies, use dependency scanning tools, maintain a software bill of materials (SBOM), and implement automated vulnerability scanning in CI/CD pipelines.', 'security_policy', ARRAY['dependencies', 'security', 'ci-cd']),
('Container Security Checklist', 'Use minimal base images, scan for vulnerabilities, run containers as non-root users, implement resource limits, and regularly update base images.', 'security_policy', ARRAY['containers', 'docker', 'security'])
ON CONFLICT DO NOTHING;

-- Insert sample scan for testing
INSERT INTO scans (target_identifier, scan_type, status, components_found, vulnerabilities_found, risk_score) VALUES
('alpine:latest', 'docker_image', 'COMPLETED', 98, 0, 0.1),
('https://github.com/example/test-repo', 'repository', 'PENDING', 0, 0, 0.0)
ON CONFLICT DO NOTHING;

-- Create indexes for better performance (if not already created)
CREATE INDEX IF NOT EXISTS idx_vulnerabilities_cve_id_lower ON vulnerabilities(LOWER(cve_id));
CREATE INDEX IF NOT EXISTS idx_knowledge_base_docs_content_type_tags ON knowledge_base_docs(content_type, tags);

-- Create a function to get vulnerability statistics
CREATE OR REPLACE FUNCTION get_vulnerability_stats()
RETURNS TABLE (
    total_vulnerabilities BIGINT,
    critical_count BIGINT,
    high_count BIGINT,
    medium_count BIGINT,
    low_count BIGINT,
    avg_cvss_score NUMERIC
) AS UTF8
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(*) as total_vulnerabilities,
        COUNT(*) FILTER (WHERE severity = 'CRITICAL') as critical_count,
        COUNT(*) FILTER (WHERE severity = 'HIGH') as high_count,
        COUNT(*) FILTER (WHERE severity = 'MEDIUM') as medium_count,
        COUNT(*) FILTER (WHERE severity = 'LOW') as low_count,
        AVG(cvss_score) as avg_cvss_score
    FROM vulnerabilities;
END;
UTF8 LANGUAGE plpgsql;

-- Create a function to search components by name
CREATE OR REPLACE FUNCTION search_components(search_term TEXT)
RETURNS TABLE (
    id UUID,
    name TEXT,
    version TEXT,
    type component_type,
    purl TEXT
) AS UTF8
BEGIN
    RETURN QUERY
    SELECT 
        sc.id,
        sc.name,
        sc.version,
        sc.type,
        sc.purl
    FROM sbom_components sc
    WHERE sc.name ILIKE '%' || search_term || '%'
       OR sc.purl ILIKE '%' || search_term || '%'
    ORDER BY sc.name, sc.version;
END;
UTF8 LANGUAGE plpgsql;

-- Create a function to get scan summary
CREATE OR REPLACE FUNCTION get_scan_summary(scan_uuid UUID)
RETURNS TABLE (
    scan_id UUID,
    target_identifier TEXT,
    scan_type TEXT,
    status scan_status,
    components_found INTEGER,
    vulnerabilities_found INTEGER,
    risk_score NUMERIC,
    duration_seconds NUMERIC
) AS UTF8
BEGIN
    RETURN QUERY
    SELECT 
        s.id,
        s.target_identifier,
        s.scan_type,
        s.status,
        s.components_found,
        s.vulnerabilities_found,
        s.risk_score,
        EXTRACT(EPOCH FROM (s.completed_at - s.initiated_at)) as duration_seconds
    FROM scans s
    WHERE s.id = scan_uuid;
END;
UTF8 LANGUAGE plpgsql;

-- Grant execute permissions on functions
GRANT EXECUTE ON FUNCTION get_vulnerability_stats() TO sbomai_user;
GRANT EXECUTE ON FUNCTION search_components(TEXT) TO sbomai_user;
GRANT EXECUTE ON FUNCTION get_scan_summary(UUID) TO sbomai_user;

-- Insert audit log entry for initial setup
INSERT INTO audit_logs (action, entity_type, details) VALUES
('DATABASE_INITIALIZED', 'system', '{"version": "1.0.0", "timestamp": "2025-08-05T00:00:00Z"}');
