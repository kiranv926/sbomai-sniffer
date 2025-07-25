package com.sbomai.vulnscan;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Main application class for the SBOMAI Vulnerability Scanner module.
 * This module handles vulnerability scanning of SBOM components against various databases.
 */
@SpringBootApplication
public class SbomaiVulnscanApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(SbomaiVulnscanApplication.class, args);
    }
} 