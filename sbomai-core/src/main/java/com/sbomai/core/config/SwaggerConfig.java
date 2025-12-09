package com.sbomai.core.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import io.swagger.v3.oas.models.servers.Server;
import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.security.SecurityScheme;
import io.swagger.v3.oas.models.security.SecurityRequirement;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;

/**
 * Swagger/OpenAPI Configuration
 * Provides interactive API documentation for the SBOMAI Core service
 */
@Configuration
public class SwaggerConfig {

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("SBOMAI Core API")
                        .description("""
                            Comprehensive API for Software Bill of Materials (SBOM) analysis and AI-powered security insights.
                            
                            ## Features
                            - **AI-Powered Analysis**: Advanced machine learning models for vulnerability detection
                            - **SBOM Processing**: Support for multiple SBOM formats (CycloneDX, SPDX, JSON)
                            - **Security Insights**: Real-time security posture assessment
                            - **Risk Assessment**: AI-driven risk scoring and recommendations
                            - **Portfolio Management**: Multi-project vulnerability tracking
                            - **Compliance Monitoring**: Automated compliance checking and reporting
                            
                            ## Authentication
                            This API supports multiple authentication methods:
                            - API Key authentication (X-API-Key header)
                            - OAuth2 with JWT tokens (Bearer token)
                            - Basic authentication (for development)
                            
                            ## Rate Limiting
                            - Standard tier: 1000 requests/hour
                            - Premium tier: 10000 requests/hour
                            - Enterprise tier: Unlimited
                            
                            ## Support
                            For API support, contact: api-support@sbomai.com
                            
                            ## API Version
                            Current API version: v1
                            Base path: /api/v1
                            """)
                        .version("1.0.0")
                        .contact(new Contact()
                                .name("SBOMAI Development Team")
                                .email("dev@sbomai.com")
                                .url("https://github.com/sbomai/sbomai-core"))
                        .license(new License()
                                .name("MIT License")
                                .url("https://opensource.org/licenses/MIT")))
                .servers(List.of(
                        new Server()
                                .url("http://localhost:8081/api/v1")
                                .description("Development Server (Local)"),
                        new Server()
                                .url("https://api.sbomai.com/v1")
                                .description("Production Server"),
                        new Server()
                                .url("https://staging-api.sbomai.com/v1")
                                .description("Staging Server")
                ))
                .components(new Components()
                        .addSecuritySchemes("apiKey", new SecurityScheme()
                                .type(SecurityScheme.Type.APIKEY)
                                .in(SecurityScheme.In.HEADER)
                                .name("X-API-Key")
                                .description("API Key for authentication. Include in header as: X-API-Key: your-api-key"))
                        .addSecuritySchemes("bearerAuth", new SecurityScheme()
                                .type(SecurityScheme.Type.HTTP)
                                .scheme("bearer")
                                .bearerFormat("JWT")
                                .description("JWT token for authentication. Include in header as: Authorization: Bearer <token>"))
                        .addSecuritySchemes("basicAuth", new SecurityScheme()
                                .type(SecurityScheme.Type.HTTP)
                                .scheme("basic")
                                .description("Basic authentication (username/password). For development use only.")))
                .addSecurityItem(new SecurityRequirement().addList("apiKey"))
                .addSecurityItem(new SecurityRequirement().addList("bearerAuth"));
    }
}

