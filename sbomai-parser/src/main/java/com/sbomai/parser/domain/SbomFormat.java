package com.sbomai.parser.domain;

/**
 * Enumeration of supported SBOM formats.
 */
public enum SbomFormat {
    SPDX("SPDX", "Software Package Data Exchange"),
    CYCLONEDX("CycloneDX", "CycloneDX Software Bill of Materials"),
    SWID("SWID", "Software Identification Tags");
    
    private final String name;
    private final String description;
    
    SbomFormat(String name, String description) {
        this.name = name;
        this.description = description;
    }
    
    public String getName() {
        return name;
    }
    
    public String getDescription() {
        return description;
    }
    
    @Override
    public String toString() {
        return name;
    }
} 