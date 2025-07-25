package com.sbomai.core.domain;

/**
 * Enumeration of supported SBOM formats.
 */
public enum SbomFormat {
    SPDX("SPDX", "Software Package Data Exchange"),
    CYCLONEDX("CycloneDX", "CycloneDX BOM Standard"),
    SWID("SWID", "Software Identification Tags");

    private final String code;
    private final String description;

    SbomFormat(String code, String description) {
        this.code = code;
        this.description = description;
    }

    public String getCode() {
        return code;
    }

    public String getDescription() {
        return description;
    }

    public static SbomFormat fromCode(String code) {
        for (SbomFormat format : values()) {
            if (format.code.equalsIgnoreCase(code)) {
                return format;
            }
        }
        throw new IllegalArgumentException("Unknown SBOM format: " + code);
    }
} 