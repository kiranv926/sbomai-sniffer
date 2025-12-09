-- SBOM AI Database Schema Initialization
-- This script creates the initial database schema for the SBOM AI application

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create projects table
CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    version VARCHAR(50) NOT NULL,
    latest_version VARCHAR(50),
    classifier VARCHAR(100) NOT NULL,
    last_bom_import TIMESTAMP,
    bom_format VARCHAR(50),
    risk_score INTEGER DEFAULT 0,
    active BOOLEAN DEFAULT true,
    policy_violations INTEGER DEFAULT 0,
    vulnerabilities INTEGER DEFAULT 0,
    last_modified DATE DEFAULT CURRENT_DATE,
    created_by VARCHAR(255),
    team VARCHAR(255),
    language VARCHAR(100),
    repo_url VARCHAR(500),
    repo_type VARCHAR(50),
    repo_branch VARCHAR(100),
    status VARCHAR(50) DEFAULT 'ACTIVE',
    critical_count INTEGER DEFAULT 0,
    high_count INTEGER DEFAULT 0,
    medium_count INTEGER DEFAULT 0,
    low_count INTEGER DEFAULT 0,
    dependency_count INTEGER DEFAULT 0,
    outdated_deps INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create project tags table
CREATE TABLE IF NOT EXISTS project_tags (
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    tag VARCHAR(255),
    PRIMARY KEY (project_id, tag)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_projects_name ON projects(name);
CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);
CREATE INDEX IF NOT EXISTS idx_projects_team ON projects(team);
CREATE INDEX IF NOT EXISTS idx_projects_active ON projects(active);
CREATE INDEX IF NOT EXISTS idx_projects_risk_score ON projects(risk_score);
CREATE INDEX IF NOT EXISTS idx_projects_created_at ON projects(created_at);
CREATE INDEX IF NOT EXISTS idx_projects_updated_at ON projects(updated_at);

-- Create full-text search index
CREATE INDEX IF NOT EXISTS idx_projects_search ON projects USING gin(to_tsvector('english', name || ' ' || COALESCE(description, '')));

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
CREATE TRIGGER update_projects_updated_at 
    BEFORE UPDATE ON projects 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Create function to update last_modified
CREATE OR REPLACE FUNCTION update_last_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_modified = CURRENT_DATE;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update last_modified
CREATE TRIGGER update_projects_last_modified 
    BEFORE UPDATE ON projects 
    FOR EACH ROW 
    EXECUTE FUNCTION update_last_modified_column();

-- Insert sample data for testing
INSERT INTO projects (name, description, version, classifier, team, language, created_by) VALUES
('sbomai-ui', 'SBOM AI-powered security analysis UI', '1.0.0', 'Application', 'Frontend Team', 'TypeScript', 'John Doe'),
('sbomai-core', 'Core engine for SBOM analysis orchestration', '1.0.0', 'Application', 'Backend Team', 'Java', 'Jane Smith'),
('sbomai-parser-go', 'Go-based SBOM parser and analyzer', '1.0.0', 'Library', 'Backend Team', 'Go', 'Mike Johnson')
ON CONFLICT (name) DO NOTHING;

-- Insert sample tags
INSERT INTO project_tags (project_id, tag) 
SELECT p.id, t.tag
FROM projects p
CROSS JOIN (VALUES 
    ('frontend'), ('react'), ('security'), ('ui'), ('typescript'),
    ('backend'), ('java'), ('spring'), ('api'), ('microservices'),
    ('parser'), ('go'), ('sbom'), ('analysis'), ('security')
) AS t(tag)
WHERE p.name = 'sbomai-ui' AND t.tag IN ('frontend', 'react', 'security', 'ui', 'typescript')
   OR p.name = 'sbomai-core' AND t.tag IN ('backend', 'java', 'spring', 'api', 'microservices')
   OR p.name = 'sbomai-parser-go' AND t.tag IN ('parser', 'go', 'sbom', 'analysis', 'security')
ON CONFLICT DO NOTHING;

-- Create view for project statistics
CREATE OR REPLACE VIEW project_statistics AS
SELECT 
    COUNT(*) as total_projects,
    COUNT(*) FILTER (WHERE active = true) as active_projects,
    COUNT(*) FILTER (WHERE vulnerabilities > 0) as projects_with_vulnerabilities,
    AVG(risk_score) FILTER (WHERE active = true) as average_risk_score,
    SUM(critical_count) as total_critical_vulnerabilities,
    SUM(high_count) as total_high_vulnerabilities,
    SUM(medium_count) as total_medium_vulnerabilities,
    SUM(low_count) as total_low_vulnerabilities,
    SUM(dependency_count) as total_dependencies,
    SUM(outdated_deps) as total_outdated_dependencies
FROM projects;

-- Create view for team statistics
CREATE OR REPLACE VIEW team_statistics AS
SELECT 
    team,
    COUNT(*) as project_count,
    AVG(risk_score) as average_risk_score,
    SUM(vulnerabilities) as total_vulnerabilities,
    SUM(dependency_count) as total_dependencies
FROM projects 
WHERE team IS NOT NULL
GROUP BY team
ORDER BY project_count DESC;

-- Grant permissions (adjust as needed for your environment)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO sbomai_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO sbomai_user;
-- GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO sbomai_user; 