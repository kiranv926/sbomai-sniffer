package com.sbomai.common.domain;

/**
 * Enumeration of supported SBOM formats
 */
public enum SbomFormat {
    SPDX("SPDX", "Software Package Data Exchange"),
    CYCLONEDX("CycloneDX", "CycloneDX"),
    SWID("SWID", "Software Identification Tags"),
    UNKNOWN("Unknown", "Unknown format");
    
    private final String displayName;
    private final String description;
    
    SbomFormat(String displayName, String description) {
        this.displayName = displayName;
        this.description = description;
    }
    
    public String getDisplayName() {
        return displayName;
    }
    
    public String getDescription() {
        return description;
    }
    
    public static SbomFormat fromString(String format) {
        if (format == null) {
            return UNKNOWN;
        }
        
        String upperFormat = format.toUpperCase();
        switch (upperFormat) {
            case "SPDX":
                return SPDX;
            case "CYCLONEDX":
            case "CYCLONE_DX":
            case "CYCLONE-DX":
                return CYCLONEDX;
            case "SWID":
                return SWID;
            default:
                return UNKNOWN;
        }
    }
    
    @Override
    public String toString() {
        return displayName;
    }
} 