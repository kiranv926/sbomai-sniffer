package com.sbomai.core.domain;

/**
 * Enumeration of vulnerability severity levels.
 */
public enum Severity {
    CRITICAL("Critical", 9.0, 10.0),
    HIGH("High", 7.0, 8.9),
    MEDIUM("Medium", 4.0, 6.9),
    LOW("Low", 0.1, 3.9),
    NONE("None", 0.0, 0.0);

    private final String displayName;
    private final double minScore;
    private final double maxScore;

    Severity(String displayName, double minScore, double maxScore) {
        this.displayName = displayName;
        this.minScore = minScore;
        this.maxScore = maxScore;
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

    public static Severity fromCvssScore(double cvssScore) {
        for (Severity severity : values()) {
            if (cvssScore >= severity.minScore && cvssScore <= severity.maxScore) {
                return severity;
            }
        }
        return NONE;
    }
} 