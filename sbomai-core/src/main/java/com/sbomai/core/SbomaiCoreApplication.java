package com.sbomai.core;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

@SpringBootApplication
@ComponentScan(basePackages = {
    "com.sbomai.core"
})
@EntityScan(basePackages = {
    "com.sbomai.core.domain"
})
@EnableJpaRepositories(basePackages = {
    "com.sbomai.core.repository"
})
public class SbomaiCoreApplication {

    public static void main(String[] args) {
        SpringApplication.run(SbomaiCoreApplication.class, args);
    }
}
