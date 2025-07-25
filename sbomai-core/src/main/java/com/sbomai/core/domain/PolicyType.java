package com.sbomai.core.domain;

/**
 * Enumeration of policy violation types.
 */
public enum PolicyType {
    LICENSE("License Policy", "License compliance and restrictions"),
    SECURITY("Security Policy", "Security vulnerability thresholds"),
    COMPONENT("Component Policy", "Component usage restrictions"),
    VERSION("Version Policy", "Version constraints and requirements"),
    SUPPLIER("Supplier Policy", "Supplier trust and verification"),
    CUSTOM("Custom Policy", "Custom business rules");

    private final String displayName;
    private final String description;

    PolicyType(String displayName, String description) {
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