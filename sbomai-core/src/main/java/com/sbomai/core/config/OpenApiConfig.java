package com.sbomai.core.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;

@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI customOpenAPI() { 
        return new OpenAPI().info(new Info()
            .title("SBOMAI Core API")
            .description("AI-Powered SBOM Analysis and Vulnerability Detection Platform")
            .version("1.0.0")
            .contact(new Contact()
                .name("SBOMAI Team")
                .email("support@sbomai.com")
                .url("https://sbomai.com")
            )
        );
    }
}
