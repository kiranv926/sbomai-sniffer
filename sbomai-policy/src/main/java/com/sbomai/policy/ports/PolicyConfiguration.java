package com.sbomai.policy.ports;

import java.util.List;
import java.util.Map;

/**
 * Configuration for policy enforcement.
 */
public class PolicyConfiguration {
    
    private final List<String> enabledPolicies;
    private final boolean strictMode;
    private final Map<String, Object> policySettings;
    private final boolean failOnBlockingViolations;
    private final int maxViolationsPerComponent;
    
    public PolicyConfiguration(List<String> enabledPolicies, boolean strictMode, 
                             Map<String, Object> policySettings, boolean failOnBlockingViolations,
                             int maxViolationsPerComponent) {
        this.enabledPolicies = enabledPolicies;
        this.strictMode = strictMode;
        this.policySettings = policySettings;
        this.failOnBlockingViolations = failOnBlockingViolations;
        this.maxViolationsPerComponent = maxViolationsPerComponent;
    }
    
    public List<String> getEnabledPolicies() { return enabledPolicies; }
    public boolean isStrictMode() { return strictMode; }
    public Map<String, Object> getPolicySettings() { return policySettings; }
    public boolean isFailOnBlockingViolations() { return failOnBlockingViolations; }
    public int getMaxViolationsPerComponent() { return maxViolationsPerComponent; }
    
    @Override
    public String toString() {
        return String.format("PolicyConfiguration{enabledPolicies=%s, strictMode=%s, failOnBlocking=%s, maxViolations=%d}",
                enabledPolicies, strictMode, failOnBlockingViolations, maxViolationsPerComponent);
    }
} 