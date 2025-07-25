package com.sbomai.policy;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Main application class for the SBOMAI Policy Enforcer module.
 * This module handles policy enforcement for SBOM components.
 */
@SpringBootApplication
public class SbomaiPolicyApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(SbomaiPolicyApplication.class, args);
    }
} 