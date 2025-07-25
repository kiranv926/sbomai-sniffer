package com.sbomai.policy.ports;

import com.sbomai.policy.domain.PolicyViolation;
import com.sbomai.policy.domain.PolicyType;

import java.util.List;
import java.util.Map;

/**
 * Port interface for policy enforcement operations.
 * This defines the contract for enforcing policies on SBOM components.
 */
public interface PolicyEnforcer {
    
    /**
     * Enforce all policies on a component.
     * 
     * @param componentData Component data to check against policies
     * @return List of policy violations found
     * @throws PolicyEnforcementException if enforcement fails
     */
    List<PolicyViolation> enforcePolicies(Map<String, Object> componentData) throws PolicyEnforcementException;
    
    /**
     * Enforce a specific policy type on a component.
     * 
     * @param componentData Component data to check against policies
     * @param policyType The type of policy to enforce
     * @return List of policy violations found
     * @throws PolicyEnforcementException if enforcement fails
     */
    List<PolicyViolation> enforcePolicy(Map<String, Object> componentData, PolicyType policyType) 
            throws PolicyEnforcementException;
    
    /**
     * Enforce a specific policy by name on a component.
     * 
     * @param componentData Component data to check against policies
     * @param policyName The name of the policy to enforce
     * @return List of policy violations found
     * @throws PolicyEnforcementException if enforcement fails
     */
    List<PolicyViolation> enforcePolicyByName(Map<String, Object> componentData, String policyName) 
            throws PolicyEnforcementException;
    
    /**
     * Validate a component against all policies without enforcing.
     * 
     * @param componentData Component data to validate
     * @return True if the component passes all policies, false otherwise
     * @throws PolicyEnforcementException if validation fails
     */
    boolean validateComponent(Map<String, Object> componentData) throws PolicyEnforcementException;
    
    /**
     * Get the current policy configuration.
     * 
     * @return Policy configuration
     */
    PolicyConfiguration getPolicyConfiguration();
    
    /**
     * Update the policy configuration.
     * 
     * @param configuration The new policy configuration
     * @throws PolicyEnforcementException if configuration update fails
     */
    void updatePolicyConfiguration(PolicyConfiguration configuration) throws PolicyEnforcementException;
    
    /**
     * Get a list of all available policies.
     * 
     * @return List of available policies
     */
    List<String> getAvailablePolicies();
    
    /**
     * Check if a specific policy is enabled.
     * 
     * @param policyName The name of the policy to check
     * @return True if the policy is enabled, false otherwise
     */
    boolean isPolicyEnabled(String policyName);
    
    /**
     * Enable or disable a specific policy.
     * 
     * @param policyName The name of the policy
     * @param enabled True to enable, false to disable
     * @throws PolicyEnforcementException if the operation fails
     */
    void setPolicyEnabled(String policyName, boolean enabled) throws PolicyEnforcementException;
} 