package com.sbomai.parser.domain;

import java.util.UUID;

/**
 * Domain model representing a relationship between SBOM components.
 */
public class SbomRelationship {
    
    private UUID id;
    private UUID sourceComponentId;
    private UUID targetComponentId;
    private RelationshipType type;
    private String description;
    
    // Constructors
    public SbomRelationship() {}
    
    public SbomRelationship(UUID sourceComponentId, UUID targetComponentId, RelationshipType type) {
        this.id = UUID.randomUUID();
        this.sourceComponentId = sourceComponentId;
        this.targetComponentId = targetComponentId;
        this.type = type;
    }
    
    // Getters and Setters
    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }
    
    public UUID getSourceComponentId() { return sourceComponentId; }
    public void setSourceComponentId(UUID sourceComponentId) { this.sourceComponentId = sourceComponentId; }
    
    public UUID getTargetComponentId() { return targetComponentId; }
    public void setTargetComponentId(UUID targetComponentId) { this.targetComponentId = targetComponentId; }
    
    public RelationshipType getType() { return type; }
    public void setType(RelationshipType type) { this.type = type; }
    
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    
    @Override
    public String toString() {
        return String.format("SbomRelationship{id=%s, source=%s, target=%s, type=%s}",
                id, sourceComponentId, targetComponentId, type);
    }
    
    /**
     * Enumeration of relationship types between SBOM components.
     */
    public enum RelationshipType {
        DEPENDS_ON("depends_on", "Component depends on another component"),
        CONTAINS("contains", "Component contains another component"),
        DESCRIBES("describes", "Component describes another component"),
        COPY_OF("copy_of", "Component is a copy of another component"),
        PATCH_FOR("patch_for", "Component is a patch for another component"),
        DYNAMIC_LINK("dynamic_link", "Component dynamically links to another component"),
        STATIC_LINK("static_link", "Component statically links to another component"),
        DATA_FILE_OF("data_file_of", "Component is a data file of another component"),
        TEST_OF("test_of", "Component is a test of another component"),
        BUILD_TOOL_OF("build_tool_of", "Component is a build tool of another component"),
        DEV_TOOL_OF("dev_tool_of", "Component is a development tool of another component"),
        TEST_TOOL_OF("test_tool_of", "Component is a test tool of another component"),
        DOCUMENTATION_OF("documentation_of", "Component is documentation of another component"),
        OPTIONAL_COMPONENT_OF("optional_component_of", "Component is optional for another component"),
        METAFILE_OF("metafile_of", "Component is a metafile of another component"),
        PACKAGE_OF("package_of", "Component is a package of another component"),
        AMENDS("amends", "Component amends another component"),
        PREREQUISITE_FOR("prerequisite_for", "Component is a prerequisite for another component"),
        HAS_PREREQUISITE("has_prerequisite", "Component has a prerequisite"),
        OTHER("other", "Other relationship type");
        
        private final String value;
        private final String description;
        
        RelationshipType(String value, String description) {
            this.value = value;
            this.description = description;
        }
        
        public String getValue() { return value; }
        public String getDescription() { return description; }
        
        @Override
        public String toString() { return value; }
    }
} 