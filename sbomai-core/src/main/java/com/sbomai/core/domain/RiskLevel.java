package com.sbomai.core.domain;

/**
 * Enumeration of AI analysis risk levels.
 */
public enum RiskLevel {
    CRITICAL("Critical", 9.0, 10.0, "Immediate action required"),
    HIGH("High", 7.0, 8.9, "High priority attention needed"),
    MEDIUM("Medium", 4.0, 6.9, "Moderate risk, review recommended"),
    LOW("Low", 0.1, 3.9, "Low risk, monitor if needed"),
    NONE("None", 0.0, 0.0, "No significant risk identified");

    private final String displayName;
    private final double minScore;
    private final double maxScore;
    private final String description;

    RiskLevel(String displayName, double minScore, double maxScore, String description) {
        this.displayName = displayName;
        this.minScore = minScore;
        this.maxScore = maxScore;
        this.description = description;
    }

    public String getDisplayName() {
        return displayName;
    }

    public double getMinScore() {
        return minScore;
    }

    public double getMaxScore() {
        return maxScore;
    }

    public String getDescription() {
        return description;
    }

    public static RiskLevel fromScore(double score) {
        for (RiskLevel level : values()) {
            if (score >= level.minScore && score <= level.maxScore) {
                return level;
            }
        }
        return NONE;
    }
} 