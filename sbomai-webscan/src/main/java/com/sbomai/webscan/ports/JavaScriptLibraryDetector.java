package com.sbomai.webscan.ports;

import com.sbomai.webscan.domain.JavaScriptLibrary;
import java.util.List;

/**
 * Interface for detecting JavaScript libraries in web pages.
 */
public interface JavaScriptLibraryDetector {

    /**
     * Detects JavaScript libraries in HTML content.
     * 
     * @param htmlContent The HTML content to analyze
     * @return List of detected JavaScript libraries
     */
    List<JavaScriptLibrary> detectLibraries(String htmlContent);

    /**
     * Detects JavaScript libraries from a list of script URLs.
     * 
     * @param scriptUrls List of script URLs to analyze
     * @return List of detected JavaScript libraries
     */
    List<JavaScriptLibrary> detectLibrariesFromUrls(List<String> scriptUrls);

    /**
     * Checks if a specific library version is outdated.
     * 
     * @param libraryName The name of the library
     * @param version The version to check
     * @return true if the version is outdated, false otherwise
     */
    boolean isOutdated(String libraryName, String version);

    /**
     * Gets the latest version of a JavaScript library.
     * 
     * @param libraryName The name of the library
     * @return The latest version, or null if not found
     */
    String getLatestVersion(String libraryName);

    /**
     * Gets known vulnerabilities for a library version.
     * 
     * @param libraryName The name of the library
     * @param version The version to check
     * @return Number of known vulnerabilities
     */
    int getKnownVulnerabilities(String libraryName, String version);
} 