package com.sbomai.core.ports;

import com.sbomai.core.domain.SbomDocument;
import com.sbomai.core.domain.PolicyViolation;

import java.util.List;

/**
 * Core interface for policy enforcement operations.
 * 
 * This interface defines the contract for enforcing policies on SBOM documents,
 * including license compliance, security thresholds, and custom business rules.
 */
public interface PolicyEnforcer {

    /**
     * Enforces policies on an SBOM document.
     * 
     * @param sbomDocument The SBOM document to check against policies
     * @return List of policy violations found
     * @throws PolicyEnforcementException if policy enforcement fails
     */
    List<PolicyViolation> enforcePolicies(SbomDocument sbomDocument) throws PolicyEnforcementException;

    /**
     * Enforces specific policy types on an SBOM document.
     * 
     * @param sbomDocument The SBOM document to check against policies
     * @param policyTypes The specific policy types to enforce
     * @return List of policy violations found
     * @throws PolicyEnforcementException if policy enforcement fails
     */
    List<PolicyViolation> enforcePolicies(SbomDocument sbomDocument, String[] policyTypes) throws PolicyEnforcementException;

    /**
     * Validates if an SBOM document passes all configured policies.
     * 
     * @param sbomDocument The SBOM document to validate
     * @return true if all policies pass, false if any violations are found
     * @throws PolicyEnforcementException if policy enforcement fails
     */
    boolean validatePolicies(SbomDocument sbomDocument) throws PolicyEnforcementException;

    /**
     * Gets the available policy types for this enforcer.
     * 
     * @return Array of available policy type names
     */
    String[] getAvailablePolicyTypes();

    /**
     * Gets the policy configuration for this enforcer.
     * 
     * @return Policy configuration information
     */
    PolicyConfiguration getPolicyConfiguration();

    /**
     * Checks if the policy enforcer is available and ready to use.
     * 
     * @return true if the enforcer is available, false otherwise
     */
    boolean isAvailable();
} 