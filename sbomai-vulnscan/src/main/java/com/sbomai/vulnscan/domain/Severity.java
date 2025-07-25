package com.sbomai.vulnscan.domain;

/**
 * Enumeration of vulnerability severity levels.
 */
public enum Severity {
    CRITICAL("Critical", 9.0, 10.0, "Critical severity vulnerabilities"),
    HIGH("High", 7.0, 8.9, "High severity vulnerabilities"),
    MEDIUM("Medium", 4.0, 6.9, "Medium severity vulnerabilities"),
    LOW("Low", 0.1, 3.9, "Low severity vulnerabilities"),
    NONE("None", 0.0, 0.0, "No severity or informational");
    
    private final String name;
    private final double minScore;
    private final double maxScore;
    private final String description;
    
    Severity(String name, double minScore, double maxScore, String description) {
        this.name = name;
        this.minScore = minScore;
        this.maxScore = maxScore;
        this.description = description;
    }
    
    public String getName() { return name; }
    public double getMinScore() { return minScore; }
    public double getMaxScore() { return maxScore; }
    public String getDescription() { return description; }
    
    /**
     * Get severity level based on CVSS score.
     */
    public static Severity fromCvssScore(double score) {
        if (score >= 9.0) return CRITICAL;
        if (score >= 7.0) return HIGH;
        if (score >= 4.0) return MEDIUM;
        if (score > 0.0) return LOW;
        return NONE;
    }
    
    @Override
    public String toString() { return name; }
} 