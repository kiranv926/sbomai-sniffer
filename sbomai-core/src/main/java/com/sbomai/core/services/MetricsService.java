package com.sbomai.core.services;

import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.concurrent.TimeUnit;

/**
 * Service for tracking SBOMAI-specific metrics.
 */
@Service
public class MetricsService {

    private final MeterRegistry meterRegistry;
    
    // Counters
    private final Counter totalProjectsScanned;
    private final Counter totalCvesFound;
    private final Counter totalPolicyViolations;
    private final Counter parserErrors;
    private final Counter scannerErrors;
    private final Counter aiAnalysisErrors;
    
    // Timers
    private final Timer sbomParseTimer;
    private final Timer vulnerabilityScanTimer;
    private final Timer aiAnalysisTimer;
    private final Timer policyEnforcementTimer;

    @Autowired
    public MetricsService(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
        
        // Initialize counters
        this.totalProjectsScanned = Counter.builder("sbomai_total_projects_scanned")
            .description("Total number of projects scanned")
            .register(meterRegistry);
            
        this.totalCvesFound = Counter.builder("sbomai_total_cves_found")
            .description("Total number of CVEs found")
            .register(meterRegistry);
            
        this.totalPolicyViolations = Counter.builder("sbomai_total_policy_violations")
            .description("Total number of policy violations")
            .register(meterRegistry);
            
        this.parserErrors = Counter.builder("sbomai_parser_errors_total")
            .description("Total number of parser errors")
            .register(meterRegistry);
            
        this.scannerErrors = Counter.builder("sbomai_scanner_errors_total")
            .description("Total number of scanner errors")
            .register(meterRegistry);
            
        this.aiAnalysisErrors = Counter.builder("sbomai_ai_analysis_errors_total")
            .description("Total number of AI analysis errors")
            .register(meterRegistry);
        
        // Initialize timers
        this.sbomParseTimer = Timer.builder("sbomai_parser_parse_duration_seconds")
            .description("Time taken to parse SBOM files")
            .register(meterRegistry);
            
        this.vulnerabilityScanTimer = Timer.builder("sbomai_vulnscan_scan_duration_seconds")
            .description("Time taken to scan for vulnerabilities")
            .register(meterRegistry);
            
        this.aiAnalysisTimer = Timer.builder("sbomai_ai_analysis_duration_seconds")
            .description("Time taken for AI analysis")
            .register(meterRegistry);
            
        this.policyEnforcementTimer = Timer.builder("sbomai_policy_enforcement_duration_seconds")
            .description("Time taken for policy enforcement")
            .register(meterRegistry);
    }

    /**
     * Increment the total projects scanned counter.
     */
    public void incrementProjectsScanned() {
        totalProjectsScanned.increment();
    }

    /**
     * Increment the total CVEs found counter.
     * 
     * @param count Number of CVEs found
     */
    public void incrementCvesFound(int count) {
        totalCvesFound.increment(count);
    }

    /**
     * Increment the total policy violations counter.
     * 
     * @param count Number of policy violations
     */
    public void incrementPolicyViolations(int count) {
        totalPolicyViolations.increment(count);
    }

    /**
     * Increment the parser errors counter.
     */
    public void incrementParserErrors() {
        parserErrors.increment();
    }

    /**
     * Increment the scanner errors counter.
     */
    public void incrementScannerErrors() {
        scannerErrors.increment();
    }

    /**
     * Increment the AI analysis errors counter.
     */
    public void incrementAiAnalysisErrors() {
        aiAnalysisErrors.increment();
    }

    /**
     * Record SBOM parsing time.
     * 
     * @param timeMs Time in milliseconds
     */
    public void recordSbomParseTime(long timeMs) {
        sbomParseTimer.record(timeMs, TimeUnit.MILLISECONDS);
    }

    /**
     * Record vulnerability scan time.
     * 
     * @param timeMs Time in milliseconds
     */
    public void recordVulnerabilityScanTime(long timeMs) {
        vulnerabilityScanTimer.record(timeMs, TimeUnit.MILLISECONDS);
    }

    /**
     * Record AI analysis time.
     * 
     * @param timeMs Time in milliseconds
     */
    public void recordAiAnalysisTime(long timeMs) {
        aiAnalysisTimer.record(timeMs, TimeUnit.MILLISECONDS);
    }

    /**
     * Record policy enforcement time.
     * 
     * @param timeMs Time in milliseconds
     */
    public void recordPolicyEnforcementTime(long timeMs) {
        policyEnforcementTimer.record(timeMs, TimeUnit.MILLISECONDS);
    }

    /**
     * Get the SBOM parse timer for manual timing.
     * 
     * @return Timer instance
     */
    public Timer.Sample startSbomParseTimer() {
        return Timer.start(meterRegistry);
    }

    /**
     * Get the vulnerability scan timer for manual timing.
     * 
     * @return Timer instance
     */
    public Timer.Sample startVulnerabilityScanTimer() {
        return Timer.start(meterRegistry);
    }

    /**
     * Get the AI analysis timer for manual timing.
     * 
     * @return Timer instance
     */
    public Timer.Sample startAiAnalysisTimer() {
        return Timer.start(meterRegistry);
    }

    /**
     * Get the policy enforcement timer for manual timing.
     * 
     * @return Timer instance
     */
    public Timer.Sample startPolicyEnforcementTimer() {
        return Timer.start(meterRegistry);
    }
} 