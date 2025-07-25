package com.sbomai.policy.ports;

/**
 * Exception thrown when policy enforcement fails.
 */
public class PolicyEnforcementException extends Exception {
    
    public PolicyEnforcementException(String message) {
        super(message);
    }
    
    public PolicyEnforcementException(String message, Throwable cause) {
        super(message, cause);
    }
    
    public PolicyEnforcementException(Throwable cause) {
        super(cause);
    }
} 