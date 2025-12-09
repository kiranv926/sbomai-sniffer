package com.sbomai.core.service;

import com.sbomai.core.dto.ScanDto;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.util.List;
import java.util.UUID;

public interface ScanService {
    
    /**
     * Get all scans with filtering and pagination
     */
    Page<ScanDto> getScans(String search, String status, String scanType, UUID projectId, Pageable pageable);
    
    /**
     * Get scan by ID
     */
    ScanDto getScan(UUID id);
    
    /**
     * Get scans by project ID
     */
    Page<ScanDto> getScansByProject(UUID projectId, String status, String scanType, Pageable pageable);
    
    /**
     * Create new scan
     */
    ScanDto createScan(ScanDto scanDto);
    
    /**
     * Update scan
     */
    ScanDto updateScan(UUID id, ScanDto scanDto);
    
    /**
     * Delete scan
     */
    void deleteScan(UUID id);
    
    /**
     * Start scan
     */
    ScanDto startScan(UUID id);
    
    /**
     * Stop scan
     */
    ScanDto stopScan(UUID id);
    
    /**
     * Get scan status
     */
    String getScanStatus(UUID id);
    
    /**
     * Get scan progress
     */
    ScanProgress getScanProgress(UUID id);
    
    /**
     * Get scan results
     */
    ScanResults getScanResults(UUID id);
    
    /**
     * Get scan statistics
     */
    ScanStatistics getScanStatistics();
    
    /**
     * Get scan trends
     */
    List<ScanTrend> getScanTrends(int days);
    
    /**
     * Bulk delete scans
     */
    void bulkDeleteScans(List<UUID> ids);
    
    /**
     * Retry failed scan
     */
    ScanDto retryScan(UUID id);
    
    /**
     * Get scan logs
     */
    List<ScanLog> getScanLogs(UUID id);
    
    /**
     * Scan progress data class
     */
    record ScanProgress(
        UUID scanId,
        String status,
        int progressPercentage,
        String currentStep,
        String estimatedTimeRemaining,
        long processedItems,
        long totalItems
    ) {}
    
    /**
     * Scan results data class
     */
    record ScanResults(
        UUID scanId,
        String status,
        long vulnerabilitiesFound,
        long componentsScanned,
        long policyViolations,
        double riskScore,
        String summary,
        List<String> recommendations
    ) {}
    
    /**
     * Scan statistics data class
     */
    record ScanStatistics(
        long totalScans,
        long completedScans,
        long failedScans,
        long runningScans,
        long pendingScans,
        double averageScanDuration,
        long totalVulnerabilitiesFound,
        long totalComponentsScanned
    ) {}
    
    /**
     * Scan trend data class
     */
    record ScanTrend(
        String date,
        long completed,
        long failed,
        long running,
        long total
    ) {}
    
    /**
     * Scan log data class
     */
    record ScanLog(
        String timestamp,
        String level,
        String message,
        String details
    ) {}
} 