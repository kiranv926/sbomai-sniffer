package com.sbomai.webscan.domain;

/**
 * Enum representing the overall security score of a website scan.
 */
public enum SecurityScore {
    EXCELLENT("Excellent", 90, 100, "The website has excellent security posture with minimal issues."),
    GOOD("Good", 80, 89, "The website has good security with minor issues that should be addressed."),
    FAIR("Fair", 70, 79, "The website has fair security with some issues that need attention."),
    POOR("Poor", 60, 69, "The website has poor security with significant issues requiring immediate attention."),
    CRITICAL("Critical", 0, 59, "The website has critical security issues that pose serious risks.");

    private final String displayName;
    private final int minScore;
    private final int maxScore;
    private final String description;

    SecurityScore(String displayName, int minScore, int maxScore, String description) {
        this.displayName = displayName;
        this.minScore = minScore;
        this.maxScore = maxScore;
        this.description = description;
    }

    public String getDisplayName() {
        return displayName;
    }

    public int getMinScore() {
        return minScore;
    }

    public int getMaxScore() {
        return maxScore;
    }

    public String getDescription() {
        return description;
    }

    public static SecurityScore fromScore(int score) {
        for (SecurityScore securityScore : values()) {
            if (score >= securityScore.minScore && score <= securityScore.maxScore) {
                return securityScore;
            }
        }
        return CRITICAL; // Default fallback
    }

    public boolean isAcceptable() {
        return this == EXCELLENT || this == GOOD;
    }

    public boolean requiresAttention() {
        return this == FAIR || this == POOR || this == CRITICAL;
    }

    public boolean isCritical() {
        return this == CRITICAL;
    }
} 