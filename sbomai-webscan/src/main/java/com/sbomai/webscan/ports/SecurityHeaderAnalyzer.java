package com.sbomai.webscan.ports;

import com.sbomai.webscan.domain.SecurityHeader;
import java.util.List;
import java.util.Map;

/**
 * Interface for analyzing security headers in HTTP responses.
 */
public interface SecurityHeaderAnalyzer {

    /**
     * Analyzes security headers from HTTP response headers.
     * 
     * @param headers Map of HTTP headers to analyze
     * @return List of security header analysis results
     */
    List<SecurityHeader> analyzeHeaders(Map<String, String> headers);

    /**
     * Analyzes a specific security header.
     * 
     * @param headerName The name of the header
     * @param headerValue The value of the header
     * @return Security header analysis result
     */
    SecurityHeader analyzeHeader(String headerName, String headerValue);

    /**
     * Gets the list of critical security headers that should be present.
     * 
     * @return List of critical security header names
     */
    List<String> getCriticalHeaders();

    /**
     * Gets recommended values for security headers.
     * 
     * @return Map of header names to recommended values
     */
    Map<String, String> getRecommendedValues();

    /**
     * Validates a security header value against best practices.
     * 
     * @param headerName The name of the header
     * @param headerValue The value to validate
     * @return true if the value follows best practices, false otherwise
     */
    boolean isValidValue(String headerName, String headerValue);

    /**
     * Gets the security score for a set of headers.
     * 
     * @param headers Map of HTTP headers
     * @return Security score (0-100)
     */
    int calculateHeaderSecurityScore(Map<String, String> headers);
} 