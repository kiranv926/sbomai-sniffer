package com.sbomai.policy.domain;

import java.time.LocalDateTime;
import java.util.Map;
import java.util.UUID;

/**
 * Domain model representing a policy violation found in an SBOM component.
 */
public class PolicyViolation {
    
    private UUID id;
    private String policyName;
    private PolicyType type;
    private Severity severity;
    private String description;
    private String componentId;
    private String componentName;
    private String componentVersion;
    private boolean blocking;
    private LocalDateTime detectedAt;
    private Map<String, Object> details;
    private String remediation;
    
    // Constructors
    public PolicyViolation() {}
    
    public PolicyViolation(String policyName, PolicyType type, Severity severity, String description) {
        this.id = UUID.randomUUID();
        this.policyName = policyName;
        this.type = type;
        this.severity = severity;
        this.description = description;
        this.detectedAt = LocalDateTime.now();
    }
    
    // Getters and Setters
    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }
    
    public String getPolicyName() { return policyName; }
    public void setPolicyName(String policyName) { this.policyName = policyName; }
    
    public PolicyType getType() { return type; }
    public void setType(PolicyType type) { this.type = type; }
    
    public Severity getSeverity() { return severity; }
    public void setSeverity(Severity severity) { this.severity = severity; }
    
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    
    public String getComponentId() { return componentId; }
    public void setComponentId(String componentId) { this.componentId = componentId; }
    
    public String getComponentName() { return componentName; }
    public void setComponentName(String componentName) { this.componentName = componentName; }
    
    public String getComponentVersion() { return componentVersion; }
    public void setComponentVersion(String componentVersion) { this.componentVersion = componentVersion; }
    
    public boolean isBlocking() { return blocking; }
    public void setBlocking(boolean blocking) { this.blocking = blocking; }
    
    public LocalDateTime getDetectedAt() { return detectedAt; }
    public void setDetectedAt(LocalDateTime detectedAt) { this.detectedAt = detectedAt; }
    
    public Map<String, Object> getDetails() { return details; }
    public void setDetails(Map<String, Object> details) { this.details = details; }
    
    public String getRemediation() { return remediation; }
    public void setRemediation(String remediation) { this.remediation = remediation; }
    
    @Override
    public String toString() {
        return String.format("PolicyViolation{id=%s, policyName='%s', type=%s, severity=%s, component='%s:%s', blocking=%s}",
                id, policyName, type, severity, componentName, componentVersion, blocking);
    }
} 