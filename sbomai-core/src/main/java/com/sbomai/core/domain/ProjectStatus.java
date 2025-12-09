package com.sbomai.core.domain;

public enum ProjectStatus {
    ACTIVE("Active"),
    ARCHIVED("Archived"),
    DEPRECATED("Deprecated");
    
    private final String displayName;
    
    ProjectStatus(String displayName) {
        this.displayName = displayName;
    }
    
    public String getDisplayName() {
        return displayName;
    }
} 