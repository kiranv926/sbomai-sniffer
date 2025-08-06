-- SBOMAI Database Schema
-- PostgreSQL Database for SBOM and Vulnerability Management
-- Version: 1.0.0
-- Created: 2025-08-05

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For text search
CREATE EXTENSION IF NOT EXISTS "btree_gin"; -- For GIN indexes on JSONB

-- Create custom types
CREATE TYPE scan_status AS ENUM ('PENDING', 'SCANNING', 'ANALYZING', 'COMPLETED', 'FAILED');
CREATE TYPE vulnerability_severity AS ENUM ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO');
CREATE TYPE remediation_status AS ENUM ('OPEN', 'IN_PROGRESS', 'PATCHED', 'MITIGATED', 'WONT_FIX');
CREATE TYPE component_type AS ENUM ('library', 'application', 'operating-system', 'framework', 'container', 'file');

-- Table for storing metadata about each scan initiated
CREATE TABLE scans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    target_identifier TEXT NOT NULL, -- e.g., repo URL, image name, file path
    scan_type TEXT NOT NULL,         -- e.g., 'repository', 'docker_image', 'filesystem'
    status scan_status NOT NULL DEFAULT 'PENDING',
    initiated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    scan_duration_seconds INTEGER,
    components_found INTEGER,
    vulnerabilities_found INTEGER,
    risk_score NUMERIC(3,2),
    -- Add user_id if you implement user authentication
    -- user_id UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table for storing the raw SBOM document (JSONB)
CREATE TABLE sbom_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scan_id UUID NOT NULL REFERENCES scans(id) ON DELETE CASCADE,
    format TEXT NOT NULL,            -- e.g., 'cyclonedx', 'spdx'
    spec_version TEXT NOT NULL,
    raw_json JSONB NOT NULL,         -- Stores the complete SBOM JSON
    ingested_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table for normalized SBOM components (extracted from raw_json for faster querying)
CREATE TABLE sbom_components (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sbom_id UUID NOT NULL REFERENCES sbom_documents(id) ON DELETE CASCADE,
    bom_ref TEXT NOT NULL,           -- Component's unique BOM-Ref
    name TEXT NOT NULL,
    version TEXT,
    type component_type,
    purl TEXT,                       -- Package URL
    cpe TEXT,                        -- Common Platform Enumeration
    license_id TEXT,                 -- Primary license ID (if any)
    description TEXT,
    author TEXT,
    supplier TEXT,
    checksums JSONB,                 -- Store multiple checksums
    properties JSONB,                -- Additional properties
    external_references JSONB,       -- External references
    -- Store other frequently queried component metadata here
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE (sbom_id, bom_ref) -- A component is unique within an SBOM
);

-- Table for storing component dependencies/relationships
CREATE TABLE component_dependencies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sbom_id UUID NOT NULL REFERENCES sbom_documents(id) ON DELETE CASCADE,
    dependent_component_id UUID NOT NULL REFERENCES sbom_components(id) ON DELETE CASCADE,
    dependency_component_id UUID NOT NULL REFERENCES sbom_components(id) ON DELETE CASCADE,
    relationship_type TEXT NOT NULL, -- e.g., 'depends_on', 'contains', 'builds_from'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE (sbom_id, dependent_component_id, dependency_component_id, relationship_type)
);

-- Table for storing identified vulnerabilities
CREATE TABLE vulnerabilities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cve_id TEXT UNIQUE,              -- e.g., 'CVE-2024-12345'
    description TEXT,
    severity vulnerability_severity,
    cvss_score NUMERIC(3,1),         -- CVSS base score
    cvss_vector TEXT,
    cvss_temporal_score NUMERIC(3,1),
    cvss_environmental_score NUMERIC(3,1),
    published_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE,
    -- Source of the vulnerability data (e.g., NVD, custom feed)
    source_name TEXT,
    source_url TEXT,
    references JSONB,                -- Additional references
    affected_versions JSONB,         -- Version ranges affected
    fixed_versions JSONB,            -- Version ranges fixed
    exploit_status TEXT,             -- e.g., 'UNKNOWN', 'POC', 'EXPLOIT_AVAILABLE'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Junction table to link SBOM components to vulnerabilities
CREATE TABLE component_vulnerabilities (
    sbom_component_id UUID NOT NULL REFERENCES sbom_components(id) ON DELETE CASCADE,
    vulnerability_id UUID NOT NULL REFERENCES vulnerabilities(id) ON DELETE CASCADE,
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    remediation_status remediation_status DEFAULT 'OPEN',
    remediation_notes TEXT,
    remediation_date TIMESTAMP WITH TIME ZONE,
    risk_score NUMERIC(3,2),         -- Component-specific risk score
    exploit_probability NUMERIC(3,2), -- AI-predicted exploit probability
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (sbom_component_id, vulnerability_id)
);

-- Table for storing knowledge base documents for RAG (e.g., remediation guides, policy docs)
CREATE TABLE knowledge_base_docs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    content TEXT NOT NULL,           -- The full text of the document/chunk
    content_type TEXT,               -- e.g., 'remediation_guide', 'security_policy', 'faq'
    source_url TEXT,
    tags TEXT[],                     -- Array of tags for categorization
    embedding_vector VECTOR(1536),   -- For vector similarity search (if using pgvector)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table for storing AI analysis results
CREATE TABLE ai_analysis_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scan_id UUID NOT NULL REFERENCES scans(id) ON DELETE CASCADE,
    analysis_type TEXT NOT NULL,     -- e.g., 'vulnerability_prediction', 'risk_assessment', 'dependency_analysis'
    model_version TEXT,              -- Version of AI model used
    results JSONB NOT NULL,          -- Detailed analysis results
    confidence_score NUMERIC(3,2),   -- Confidence in the analysis
    processing_time_seconds NUMERIC(10,3),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table for storing risk assessment history
CREATE TABLE risk_assessments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scan_id UUID NOT NULL REFERENCES scans(id) ON DELETE CASCADE,
    overall_risk_score NUMERIC(3,2),
    risk_factors JSONB,              -- Detailed risk factors
    recommendations JSONB,           -- AI-generated recommendations
    assessed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table for storing audit logs
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    action TEXT NOT NULL,            -- e.g., 'SCAN_CREATED', 'VULNERABILITY_DETECTED', 'REMEDIATION_APPLIED'
    entity_type TEXT NOT NULL,       -- e.g., 'scan', 'component', 'vulnerability'
    entity_id UUID,                  -- ID of the affected entity
    details JSONB,                   -- Additional details about the action
    performed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for optimal performance
CREATE INDEX idx_scans_target_identifier ON scans(target_identifier);
CREATE INDEX idx_scans_status ON scans(status);
CREATE INDEX idx_scans_initiated_at ON scans(initiated_at);
CREATE INDEX idx_scans_created_at ON scans(created_at);

CREATE INDEX idx_sbom_documents_scan_id ON sbom_documents(scan_id);
CREATE INDEX idx_sbom_documents_format ON sbom_documents(format);
CREATE INDEX idx_sbom_documents_raw_json_gin ON sbom_documents USING GIN (raw_json);

CREATE INDEX idx_sbom_components_sbom_id ON sbom_components(sbom_id);
CREATE INDEX idx_sbom_components_name ON sbom_components(name);
CREATE INDEX idx_sbom_components_purl ON sbom_components(purl);
CREATE INDEX idx_sbom_components_type ON sbom_components(type);
CREATE INDEX idx_sbom_components_name_version ON sbom_components(name, version);

CREATE INDEX idx_component_dependencies_sbom_id ON component_dependencies(sbom_id);
CREATE INDEX idx_component_dependencies_dependent ON component_dependencies(dependent_component_id);
CREATE INDEX idx_component_dependencies_dependency ON component_dependencies(dependency_component_id);

CREATE INDEX idx_vulnerabilities_cve_id ON vulnerabilities(cve_id);
CREATE INDEX idx_vulnerabilities_severity ON vulnerabilities(severity);
CREATE INDEX idx_vulnerabilities_cvss_score ON vulnerabilities(cvss_score);
CREATE INDEX idx_vulnerabilities_published_at ON vulnerabilities(published_at);

CREATE INDEX idx_component_vulnerabilities_component ON component_vulnerabilities(sbom_component_id);
CREATE INDEX idx_component_vulnerabilities_vulnerability ON component_vulnerabilities(vulnerability_id);
CREATE INDEX idx_component_vulnerabilities_status ON component_vulnerabilities(remediation_status);
CREATE INDEX idx_component_vulnerabilities_risk_score ON component_vulnerabilities(risk_score);

CREATE INDEX idx_knowledge_base_docs_content_type ON knowledge_base_docs(content_type);
CREATE INDEX idx_knowledge_base_docs_tags ON knowledge_base_docs USING GIN (tags);

CREATE INDEX idx_ai_analysis_results_scan_id ON ai_analysis_results(scan_id);
CREATE INDEX idx_ai_analysis_results_type ON ai_analysis_results(analysis_type);

CREATE INDEX idx_risk_assessments_scan_id ON risk_assessments(scan_id);
CREATE INDEX idx_risk_assessments_risk_score ON risk_assessments(overall_risk_score);

CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_entity_type ON audit_logs(entity_type);
CREATE INDEX idx_audit_logs_performed_at ON audit_logs(performed_at);

-- Create full-text search indexes
CREATE INDEX idx_sbom_components_name_fts ON sbom_components USING GIN (to_tsvector('english', name));
CREATE INDEX idx_vulnerabilities_description_fts ON vulnerabilities USING GIN (to_tsvector('english', description));
CREATE INDEX idx_knowledge_base_docs_content_fts ON knowledge_base_docs USING GIN (to_tsvector('english', content));

-- Create updated_at triggers
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS -Force
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
-Force language 'plpgsql';

CREATE TRIGGER update_scans_updated_at BEFORE UPDATE ON scans FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_sbom_components_updated_at BEFORE UPDATE ON sbom_components FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_vulnerabilities_updated_at BEFORE UPDATE ON vulnerabilities FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_component_vulnerabilities_updated_at BEFORE UPDATE ON component_vulnerabilities FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_knowledge_base_docs_updated_at BEFORE UPDATE ON knowledge_base_docs FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create views for common queries
CREATE VIEW scan_summary AS
SELECT 
    s.id,
    s.target_identifier,
    s.scan_type,
    s.status,
    s.initiated_at,
    s.completed_at,
    s.components_found,
    s.vulnerabilities_found,
    s.risk_score,
    EXTRACT(EPOCH FROM (s.completed_at - s.initiated_at)) as duration_seconds
FROM scans s;

CREATE VIEW component_vulnerability_summary AS
SELECT 
    sc.id as component_id,
    sc.name as component_name,
    sc.version as component_version,
    sc.type as component_type,
    sc.purl,
    COUNT(cv.vulnerability_id) as vulnerability_count,
    MAX(v.severity) as highest_severity,
    AVG(cv.risk_score) as avg_risk_score,
    AVG(cv.exploit_probability) as avg_exploit_probability
FROM sbom_components sc
LEFT JOIN component_vulnerabilities cv ON sc.id = cv.sbom_component_id
LEFT JOIN vulnerabilities v ON cv.vulnerability_id = v.id
GROUP BY sc.id, sc.name, sc.version, sc.type, sc.purl;

CREATE VIEW vulnerability_summary AS
SELECT 
    v.id,
    v.cve_id,
    v.severity,
    v.cvss_score,
    v.published_at,
    COUNT(cv.sbom_component_id) as affected_components_count,
    AVG(cv.risk_score) as avg_component_risk_score
FROM vulnerabilities v
LEFT JOIN component_vulnerabilities cv ON v.id = cv.vulnerability_id
GROUP BY v.id, v.cve_id, v.severity, v.cvss_score, v.published_at;

-- Grant permissions (adjust as needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO sbomai_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO sbomai_user;
