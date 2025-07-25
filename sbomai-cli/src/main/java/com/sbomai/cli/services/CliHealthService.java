package com.sbomai.cli.services;

import com.sbomai.core.services.HealthStatus;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * Service for checking CLI system health.
 */
@Service
public class CliHealthService {

    private static final Logger logger = LoggerFactory.getLogger(CliHealthService.class);

    private final com.sbomai.core.services.SbomAnalysisOrchestrator orchestrator;
    private final RemoteApiService remoteApiService;

    @Autowired
    public CliHealthService(com.sbomai.core.services.SbomAnalysisOrchestrator orchestrator, RemoteApiService remoteApiService) {
        this.orchestrator = orchestrator;
        this.remoteApiService = remoteApiService;
    }

    /**
     * Checks the health of local services.
     * 
     * @return true if local services are healthy
     */
    public boolean checkLocalHealth() {
        try {
            HealthStatus status = orchestrator.getHealthStatus();
            return status.isFullyOperational();
        } catch (Exception e) {
            logger.error("Local health check failed", e);
            return false;
        }
    }

    /**
     * Checks the health of remote services.
     * 
     * @param remoteUrl The remote service URL
     * @return true if remote services are healthy
     */
    public boolean checkRemoteHealth(String remoteUrl) {
        try {
            return remoteApiService.checkHealth(remoteUrl);
        } catch (Exception e) {
            logger.error("Remote health check failed for URL: {}", remoteUrl, e);
            return false;
        }
    }
} 