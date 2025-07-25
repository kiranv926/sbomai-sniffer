package com.sbomai.policy.domain;

/**
 * Enumeration of policy violation severity levels.
 */
public enum Severity {
    CRITICAL("Critical", "Critical severity violations"),
    HIGH("High", "High severity violations"),
    MEDIUM("Medium", "Medium severity violations"),
    LOW("Low", "Low severity violations"),
    INFO("Info", "Informational violations");
    
    private final String name;
    private final String description;
    
    Severity(String name, String description) {
        this.name = name;
        this.description = description;
    }
    
    public String getName() { return name; }
    public String getDescription() { return description; }
    
    @Override
    public String toString() { return name; }
} 