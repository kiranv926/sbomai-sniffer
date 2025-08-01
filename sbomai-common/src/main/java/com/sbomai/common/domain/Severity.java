package com.sbomai.common.domain;

/**
 * Enumeration of vulnerability severity levels
 */
public enum Severity {
    CRITICAL(4, "Critical", "Critical severity vulnerabilities"),
    HIGH(3, "High", "High severity vulnerabilities"),
    MEDIUM(2, "Medium", "Medium severity vulnerabilities"),
    LOW(1, "Low", "Low severity vulnerabilities"),
    INFO(0, "Info", "Informational findings");
    
    private final int level;
    private final String displayName;
    private final String description;
    
    Severity(int level, String displayName, String description) {
        this.level = level;
        this.displayName = displayName;
        this.description = description;
    }
    
    public int getLevel() {
        return level;
    }
    
    public String getDisplayName() {
        return displayName;
    }
    
    public String getDescription() {
        return description;
    }
    
    public static Severity fromString(String severity) {
        if (severity == null) {
            return INFO;
        }
        
        String upperSeverity = severity.toUpperCase();
        switch (upperSeverity) {
            case "CRITICAL":
                return CRITICAL;
            case "HIGH":
                return HIGH;
            case "MEDIUM":
                return MEDIUM;
            case "LOW":
                return LOW;
            case "INFO":
            case "INFORMATION":
                return INFO;
            default:
                return INFO;
        }
    }
    
    public static Severity fromCvssScore(Double cvssScore) {
        if (cvssScore == null) {
            return INFO;
        }
        
        if (cvssScore >= 9.0) {
            return CRITICAL;
        } else if (cvssScore >= 7.0) {
            return HIGH;
        } else if (cvssScore >= 4.0) {
            return MEDIUM;
        } else if (cvssScore >= 0.1) {
            return LOW;
        } else {
            return INFO;
        }
    }
    
    public boolean isCritical() {
        return this == CRITICAL;
    }
    
    public boolean isHigh() {
        return this == HIGH || this == CRITICAL;
    }
    
    public boolean isMediumOrHigher() {
        return this.level >= MEDIUM.level;
    }
    
    @Override
    public String toString() {
        return displayName;
    }
} 