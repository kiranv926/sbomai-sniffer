package com.sbomai.webscan.domain;

/**
 * Enum representing the security status of individual components or findings.
 */
public enum SecurityStatus {
    SECURE("Secure", "The component or configuration is secure and follows best practices."),
    INSECURE("Insecure", "The component or configuration has security issues that need to be addressed."),
    WARNING("Warning", "The component or configuration has potential security concerns."),
    INFO("Information", "Informational finding that may be relevant for security assessment."),
    UNKNOWN("Unknown", "The security status could not be determined.");

    private final String displayName;
    private final String description;

    SecurityStatus(String displayName, String description) {
        this.displayName = displayName;
        this.description = description;
    }

    public String getDisplayName() {
        return displayName;
    }

    public String getDescription() {
        return description;
    }

    public boolean isSecure() {
        return this == SECURE;
    }

    public boolean isInsecure() {
        return this == INSECURE;
    }

    public boolean requiresAttention() {
        return this == INSECURE || this == WARNING;
    }
} 