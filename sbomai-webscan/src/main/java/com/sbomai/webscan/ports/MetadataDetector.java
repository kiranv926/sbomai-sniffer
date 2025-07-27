package com.sbomai.webscan.ports;

import com.sbomai.webscan.domain.ExposedMetadata;
import java.util.List;

/**
 * Interface for detecting exposed metadata in web content.
 */
public interface MetadataDetector {

    /**
     * Detects exposed metadata in HTML content.
     * 
     * @param htmlContent The HTML content to analyze
     * @return List of detected exposed metadata
     */
    List<ExposedMetadata> detectMetadata(String htmlContent);

    /**
     * Detects metadata from HTML meta tags.
     * 
     * @param htmlContent The HTML content to analyze
     * @return List of detected metadata from meta tags
     */
    List<ExposedMetadata> detectMetaTags(String htmlContent);

    /**
     * Detects metadata from HTML comments.
     * 
     * @param htmlContent The HTML content to analyze
     * @return List of detected metadata from comments
     */
    List<ExposedMetadata> detectComments(String htmlContent);

    /**
     * Detects metadata from JavaScript code.
     * 
     * @param javascriptCode The JavaScript code to analyze
     * @return List of detected metadata from JavaScript
     */
    List<ExposedMetadata> detectJavaScriptMetadata(String javascriptCode);

    /**
     * Detects metadata from HTTP headers.
     * 
     * @param headers Map of HTTP headers
     * @return List of detected metadata from headers
     */
    List<ExposedMetadata> detectHeaderMetadata(java.util.Map<String, String> headers);

    /**
     * Checks if a piece of metadata is sensitive.
     * 
     * @param key The metadata key
     * @param value The metadata value
     * @return true if the metadata is sensitive, false otherwise
     */
    boolean isSensitiveMetadata(String key, String value);

    /**
     * Gets the sensitivity level of metadata.
     * 
     * @param key The metadata key
     * @param value The metadata value
     * @return Sensitivity level
     */
    com.sbomai.webscan.domain.SensitivityLevel getSensitivityLevel(String key, String value);
} 