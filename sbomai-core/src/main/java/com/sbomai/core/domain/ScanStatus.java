package com.sbomai.core.domain;

/**
 * Enumeration of vulnerability scan statuses.
 */
public enum ScanStatus {
    PENDING("Pending", "Scan has not started yet"),
    IN_PROGRESS("In Progress", "Scan is currently running"),
    COMPLETED("Completed", "Scan completed successfully"),
    FAILED("Failed", "Scan failed with errors"),
    TIMEOUT("Timeout", "Scan timed out"),
    CANCELLED("Cancelled", "Scan was cancelled");

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
} 