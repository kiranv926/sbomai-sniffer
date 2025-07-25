package com.sbomai.policy.domain;

/**
 * Enumeration of policy types that can be enforced.
 */
public enum PolicyType {
    LICENSE("License", "License compliance policies"),
    SECURITY("Security", "Security-related policies (CVSS thresholds, etc.)"),
    COMPONENT("Component", "Component-specific policies"),
    VERSION("Version", "Version-related policies"),
    SUPPLIER("Supplier", "Supplier-related policies"),
    CUSTOM("Custom", "Custom user-defined policies");
    
    private final String name;
    private final String description;
    
    PolicyType(String name, String description) {
        this.name = name;
        this.description = description;
    }
    
    public String getName() { return name; }
    public String getDescription() { return description; }
    
    @Override
    public String toString() { return name; }
} 