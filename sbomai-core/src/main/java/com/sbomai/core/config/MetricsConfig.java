package com.sbomai.core.config;

import io.micrometer.core.aop.TimedAspect;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.simple.SimpleMeterRegistry;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Configuration for metrics and monitoring.
 */
@Configuration
public class MetricsConfig {

    /**
     * Configure TimedAspect for automatic method timing.
     * 
     * @param registry The meter registry
     * @return TimedAspect bean
     */
    @Bean
    public TimedAspect timedAspect(MeterRegistry registry) {
        return new TimedAspect(registry);
    }

    /**
     * Fallback meter registry for testing.
     * 
     * @return SimpleMeterRegistry bean
     */
    @Bean
    public MeterRegistry meterRegistry() {
        return new SimpleMeterRegistry();
    }
} 