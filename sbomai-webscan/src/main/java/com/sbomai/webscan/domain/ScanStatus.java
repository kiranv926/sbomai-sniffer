package com.sbomai.webscan.domain;

/**
 * Enum representing the status of a web scan operation.
 */
public enum ScanStatus {
    PENDING("Pending", "Scan is queued and waiting to be processed."),
    IN_PROGRESS("In Progress", "Scan is currently being executed."),
    COMPLETED("Completed", "Scan has completed successfully."),
    FAILED("Failed", "Scan has failed due to an error."),
    CANCELLED("Cancelled", "Scan was cancelled by the user."),
    TIMEOUT("Timeout", "Scan timed out during execution.");

    private final String displayName;
    private final String description;

    ScanStatus(String displayName, String description) {
        this.displayName = displayName;
        this.description = description;
    }

    public String getDisplayName() {
        return displayName;
    }

    public String getDescription() {
        return description;
    }

    public boolean isActive() {
        return this == PENDING || this == IN_PROGRESS;
    }

    public boolean isCompleted() {
        return this == COMPLETED;
    }

    public boolean isFailed() {
        return this == FAILED || this == CANCELLED || this == TIMEOUT;
    }

    public boolean isTerminal() {
        return this == COMPLETED || this == FAILED || this == CANCELLED || this == TIMEOUT;
    }
} 