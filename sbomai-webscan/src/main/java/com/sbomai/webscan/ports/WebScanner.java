package com.sbomai.webscan.ports;

import com.sbomai.webscan.domain.WebScanResult;
import java.util.concurrent.CompletableFuture;

/**
 * Core interface for website security scanning operations.
 * 
 * This interface defines the contract for scanning websites to detect:
 * - Outdated frontend JavaScript libraries
 * - Missing or insecure security headers
 * - Exposed metadata and sensitive information
 * - Common web security vulnerabilities
 */
public interface WebScanner {

    /**
     * Scans a website for security issues.
     * 
     * @param url The URL of the website to scan
     * @return CompletableFuture containing the scan result
     * @throws WebScanException if scanning fails
     */
    CompletableFuture<WebScanResult> scanWebsite(String url) throws WebScanException;

    /**
     * Scans a website with custom scan parameters.
     * 
     * @param url The URL of the website to scan
     * @param scanOptions Custom scan options and configurations
     * @return CompletableFuture containing the scan result
     * @throws WebScanException if scanning fails
     */
    CompletableFuture<WebScanResult> scanWebsite(String url, ScanOptions scanOptions) throws WebScanException;

    /**
     * Gets the scanner capabilities and supported features.
     * 
     * @return Scanner capabilities information
     */
    ScannerCapabilities getCapabilities();

    /**
     * Checks if the scanner is available and ready to use.
     * 
     * @return true if the scanner is available, false otherwise
     */
    boolean isAvailable();

    /**
     * Gets the scanner version and information.
     * 
     * @return Scanner information
     */
    ScannerInfo getScannerInfo();

    /**
     * Estimates the time required to scan a website.
     * 
     * @param url The URL to estimate scan time for
     * @return Estimated scan time in milliseconds
     */
    long estimateScanTime(String url);
} 