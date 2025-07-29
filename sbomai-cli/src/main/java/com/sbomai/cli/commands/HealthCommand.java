package com.sbomai.cli.commands;

import com.sbomai.core.services.SbomAnalysisOrchestrator;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import picocli.CommandLine;

import java.util.concurrent.Callable;

/**
 * CLI command for checking system health.
 */
@Component
@CommandLine.Command(
    name = "health",
    description = "Check the health status of SBOMAI services",
    mixinStandardHelpOptions = true
)
public class HealthCommand implements Callable<Integer> {

    @Autowired
    private SbomAnalysisOrchestrator orchestrator;

    @CommandLine.Option(
        names = {"-r", "--remote"},
        description = "Check remote SBOMAI core service health"
    )
    private boolean checkRemote;

    @CommandLine.Option(
        names = {"-u", "--url"},
        description = "Remote SBOMAI core service URL (default: http://localhost:8080)",
        defaultValue = "http://localhost:8080"
    )
    private String remoteUrl;

    @Override
    public Integer call() throws Exception {
        try {
            System.out.println("🏥 SBOMAI Health Check");
            System.out.println("=====================");

            if (checkRemote) {
                System.out.println("🌐 Checking remote service at: " + remoteUrl);
                System.out.println("⚠️  Remote health check not implemented yet");
                return 1;
            } else {
                System.out.println("🏠 Checking local service...");
                
                if (orchestrator != null) {
                    var healthStatus = orchestrator.getHealthStatus();
                    
                    System.out.println("📊 Service Status:");
                    System.out.println("  SBOM Parser: " + (healthStatus.isSbomParserAvailable() ? "✅ Available" : "❌ Unavailable"));
                    System.out.println("  Vulnerability Scanner: " + (healthStatus.isVulnerabilityScannerAvailable() ? "✅ Available" : "❌ Unavailable"));
                    System.out.println("  AI Analyzer: " + (healthStatus.isAiAnalyzerAvailable() ? "✅ Available" : "❌ Unavailable"));
                    System.out.println("  Policy Enforcer: " + (healthStatus.isPolicyEnforcerAvailable() ? "✅ Available" : "❌ Unavailable"));
                    
                    boolean overallHealthy = healthStatus.isFullyOperational();
                    if (overallHealthy) {
                        System.out.println("\n✅ All services are healthy and operational!");
                        return 0;
                    } else {
                        System.out.println("\n⚠️  Some services are unavailable");
                        return 1;
                    }
                } else {
                    System.out.println("❌ Orchestrator service not available");
                    return 1;
                }
            }

        } catch (Exception e) {
            System.err.println("❌ Health check failed: " + e.getMessage());
            return 1;
        }
    }
} 