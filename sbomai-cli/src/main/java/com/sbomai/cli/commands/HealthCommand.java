package com.sbomai.cli.commands;

import com.sbomai.cli.services.CliHealthService;
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
    private CliHealthService healthService;

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
                boolean isHealthy = healthService.checkRemoteHealth(remoteUrl);
                
                if (isHealthy) {
                    System.out.println("✅ Remote service is healthy");
                    return 0;
                } else {
                    System.out.println("❌ Remote service is unhealthy");
                    return 1;
                }
            } else {
                System.out.println("🏠 Checking local service...");
                boolean isHealthy = healthService.checkLocalHealth();
                
                if (isHealthy) {
                    System.out.println("✅ Local service is healthy");
                    return 0;
                } else {
                    System.out.println("❌ Local service is unhealthy");
                    return 1;
                }
            }

        } catch (Exception e) {
            System.err.println("❌ Health check failed: " + e.getMessage());
            return 1;
        }
    }
} 