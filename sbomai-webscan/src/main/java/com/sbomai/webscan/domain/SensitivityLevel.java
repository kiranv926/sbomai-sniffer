package com.sbomai.webscan.domain;

/**
 * Enum representing the sensitivity levels for exposed metadata and information.
 */
public enum SensitivityLevel {
    CRITICAL("Critical", "Highly sensitive information that could lead to serious security breaches."),
    HIGH("High", "Sensitive information that could be used for malicious purposes."),
    MEDIUM("Medium", "Moderately sensitive information that should be protected."),
    LOW("Low", "Low sensitivity information with minimal security impact."),
    PUBLIC("Public", "Public information that is safe to expose.");

    private final String displayName;
    private final String description;

    SensitivityLevel(String displayName, String description) {
        this.displayName = displayName;
        this.description = description;
    }

    public String getDisplayName() {
        return displayName;
    }

    public String getDescription() {
        return description;
    }

    public boolean isCritical() {
        return this == CRITICAL;
    }

    public boolean isHigh() {
        return this == HIGH;
    }

    public boolean isCriticalOrHigh() {
        return this == CRITICAL || this == HIGH;
    }

    public boolean requiresProtection() {
        return this == CRITICAL || this == HIGH || this == MEDIUM;
    }

    public boolean isSafe() {
        return this == LOW || this == PUBLIC;
    }
} 