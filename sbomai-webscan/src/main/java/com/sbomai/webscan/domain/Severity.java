package com.sbomai.webscan.domain;

/**
 * Enum representing the severity levels for vulnerabilities and security issues.
 */
public enum Severity {
    CRITICAL("Critical", 5, "Critical severity issues that pose immediate and severe risks."),
    HIGH("High", 4, "High severity issues that pose significant risks."),
    MEDIUM("Medium", 3, "Medium severity issues that pose moderate risks."),
    LOW("Low", 2, "Low severity issues that pose minimal risks."),
    INFO("Info", 1, "Informational findings that may be relevant.");

    private final String displayName;
    private final int numericValue;
    private final String description;

    Severity(String displayName, int numericValue, String description) {
        this.displayName = displayName;
        this.numericValue = numericValue;
        this.description = description;
    }

    public String getDisplayName() {
        return displayName;
    }

    public int getNumericValue() {
        return numericValue;
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

    public boolean requiresImmediateAttention() {
        return this == CRITICAL || this == HIGH;
    }

    public boolean isSignificant() {
        return this == CRITICAL || this == HIGH || this == MEDIUM;
    }
} 