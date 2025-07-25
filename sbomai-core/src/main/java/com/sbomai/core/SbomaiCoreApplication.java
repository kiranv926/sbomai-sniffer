package com.sbomai.core;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;

/**
 * Main Spring Boot application for SBOMAI Core Engine.
 * 
 * This application provides the core SBOM analysis capabilities including:
 * - SBOM parsing (SPDX, CycloneDX)
 * - Vulnerability scanning (NVD, OSS Index, OSV)
 * - AI-powered risk analysis
 * - Policy enforcement
 * 
 * The application exposes REST APIs for external modules to consume.
 */
@SpringBootApplication
@ComponentScan(basePackages = {
    "com.sbomai.core",
    "com.sbomai.parser",
    "com.sbomai.scanner", 
    "com.sbomai.ai",
    "com.sbomai.policy"
})
public class SbomaiCoreApplication {

    public static void main(String[] args) {
        SpringApplication.run(SbomaiCoreApplication.class, args);
    }
} 