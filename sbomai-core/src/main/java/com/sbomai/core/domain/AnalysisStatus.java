package com.sbomai.core.domain;

/**
 * Enumeration of SBOM analysis statuses.
 */
public enum AnalysisStatus {
    PENDING("Pending", "Analysis has not started yet"),
    IN_PROGRESS("In Progress", "Analysis is currently running"),
    COMPLETED("Completed", "Analysis completed successfully"),
    FAILED("Failed", "Analysis failed with errors"),
    PARTIAL("Partial", "Analysis completed with some failures");

    private final String displayName;
    private final String description;

    AnalysisStatus(String displayName, String description) {
        this.displayName = displayName;
        this.description = description;
    }

    public String getDisplayName() {
        return displayName;
    }

    public String getDescription() {
        return description;
    }
} 