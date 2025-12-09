package com.sbomai.core.service;

import org.springframework.web.multipart.MultipartFile;

public interface SbomParserService {
    
    /**
     * Parse SBOM file and return analysis results
     * @param file The SBOM file to parse
     * @return JSON string containing parsed results
     */
    String parseSbomFile(MultipartFile file);
    
    /**
     * Parse SBOM file from file path
     * @param filePath Path to the SBOM file
     * @return JSON string containing parsed results
     */
    String parseSbomFile(String filePath);
    
    /**
     * Validate SBOM file format
     * @param file The SBOM file to validate
     * @return true if valid, false otherwise
     */
    boolean validateSbomFormat(MultipartFile file);
    
    /**
     * Get supported SBOM formats
     * @return Array of supported format strings
     */
    String[] getSupportedFormats();
} 