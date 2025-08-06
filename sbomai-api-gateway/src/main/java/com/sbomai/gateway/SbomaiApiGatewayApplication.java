package com.sbomai.gateway;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.cloud.gateway.route.RouteLocator;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.reactive.CorsWebFilter;
import org.springframework.web.cors.reactive.UrlBasedCorsConfigurationSource;

import java.util.Arrays;

/**
 * SBOMAI API Gateway - Main entry point for all UI requests
 * 
 * This gateway routes requests to appropriate microservices and handles
 * authentication, rate limiting, and security.
 */
@SpringBootApplication
@EnableDiscoveryClient
public class SbomaiApiGatewayApplication {

    public static void main(String[] args) {
        SpringApplication.run(SbomaiApiGatewayApplication.class, args);
    }

    /**
     * Configure API routes for different microservices
     */
    @Bean
    public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
        return builder.routes()
                // Authentication Service Routes
                .route("auth-service", r -> r
                        .path("/api/auth/**")
                        .filters(f -> f
                                .rewritePath("/api/auth/(?<segment>.*)", "/${segment}")
                                .addRequestHeader("X-Response-Time", System.currentTimeMillis() + ""))
                        .uri("lb://sbomai-auth-service"))
                
                // Project Management Service Routes
                .route("project-service", r -> r
                        .path("/api/projects/**")
                        .filters(f -> f
                                .rewritePath("/api/projects/(?<segment>.*)", "/${segment}")
                                .addRequestHeader("X-Response-Time", System.currentTimeMillis() + ""))
                        .uri("lb://sbomai-project-service"))
                
                // AI Analysis Service Routes (sbomai-engine integration)
                .route("ai-analysis-service", r -> r
                        .path("/api/ai/**")
                        .filters(f -> f
                                .rewritePath("/api/ai/(?<segment>.*)", "/${segment}")
                                .addRequestHeader("X-Response-Time", System.currentTimeMillis() + ""))
                        .uri("lb://sbomai-ai-service"))
                
                // Security Scanning Service Routes
                .route("scan-service", r -> r
                        .path("/api/scans/**")
                        .filters(f -> f
                                .rewritePath("/api/scans/(?<segment>.*)", "/${segment}")
                                .addRequestHeader("X-Response-Time", System.currentTimeMillis() + ""))
                        .uri("lb://sbomai-scan-service"))
                
                // Policy Engine Service Routes
                .route("policy-service", r -> r
                        .path("/api/policies/**")
                        .filters(f -> f
                                .rewritePath("/api/policies/(?<segment>.*)", "/${segment}")
                                .addRequestHeader("X-Response-Time", System.currentTimeMillis() + ""))
                        .uri("lb://sbomai-policy-service"))
                
                // Integration Service Routes
                .route("integration-service", r -> r
                        .path("/api/integrations/**")
                        .filters(f -> f
                                .rewritePath("/api/integrations/(?<segment>.*)", "/${segment}")
                                .addRequestHeader("X-Response-Time", System.currentTimeMillis() + ""))
                        .uri("lb://sbomai-integration-service"))
                
                // Notification Service Routes
                .route("notification-service", r -> r
                        .path("/api/notifications/**")
                        .filters(f -> f
                                .rewritePath("/api/notifications/(?<segment>.*)", "/${segment}")
                                .addRequestHeader("X-Response-Time", System.currentTimeMillis() + ""))
                        .uri("lb://sbomai-notification-service"))
                
                // Chat Assistant Service Routes
                .route("chat-service", r -> r
                        .path("/api/chat/**")
                        .filters(f -> f
                                .rewritePath("/api/chat/(?<segment>.*)", "/${segment}")
                                .addRequestHeader("X-Response-Time", System.currentTimeMillis() + ""))
                        .uri("lb://sbomai-chat-service"))
                
                .build();
    }

    /**
     * Configure CORS for frontend integration
     */
    @Bean
    public CorsWebFilter corsWebFilter() {
        CorsConfiguration corsConfig = new CorsConfiguration();
        corsConfig.setAllowedOriginPatterns(Arrays.asList("*"));
        corsConfig.setAllowedMethods(Arrays.asList("GET", "POST", "PUT", "DELETE", "OPTIONS"));
        corsConfig.setAllowedHeaders(Arrays.asList("*"));
        corsConfig.setAllowCredentials(true);

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", corsConfig);

        return new CorsWebFilter(source);
    }
} 