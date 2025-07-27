package com.sbomai.webscan;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;

/**
 * Main application class for SBOMAI Web Scanner.
 * 
 * This module provides website scanning capabilities to detect:
 * - Outdated frontend JavaScript libraries
 * - Missing or insecure security headers
 * - Exposed metadata and sensitive information
 * - Common web security vulnerabilities
 */
@SpringBootApplication
@EnableAsync
public class SbomaiWebscanApplication {

    public static void main(String[] args) {
        SpringApplication.run(SbomaiWebscanApplication.class, args);
    }
} 