package com.sbomai.parser;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Main application class for the SBOMAI Parser module.
 * This module handles parsing of SBOM files in various formats (SPDX, CycloneDX, SWID).
 */
@SpringBootApplication
public class SbomaiParserApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(SbomaiParserApplication.class, args);
    }
} 