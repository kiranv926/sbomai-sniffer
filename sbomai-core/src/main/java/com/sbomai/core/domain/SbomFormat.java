package com.sbomai.core.domain;

/**
 * Enumeration of supported SBOM formats.
 */
public enum SbomFormat {
    UNKNOWN("Unknown", "Unknown format"),
    SPDX("SPDX", "Software Package Data Exchange"),
    SPDX_JSON("SPDX_JSON", "SPDX JSON format"),
    SPDX_XML("SPDX_XML", "SPDX XML format"),
    CYCLONEDX("CycloneDX", "CycloneDX BOM Standard"),
    CYCLONEDX_JSON("CYCLONEDX_JSON", "CycloneDX JSON format"),
    CYCLONEDX_XML("CYCLONEDX_XML", "CycloneDX XML format"),
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