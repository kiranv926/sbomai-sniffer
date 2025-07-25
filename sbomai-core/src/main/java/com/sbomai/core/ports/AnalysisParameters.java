package com.sbomai.core.ports;

/**
 * Parameters for AI analysis configuration.
 */
public class AnalysisParameters {
    private final String model;
    private final double confidenceThreshold;
    private final int maxTokens;
    private final double temperature;
    private final boolean includeRecommendations;

    private AnalysisParameters(Builder builder) {
        this.model = builder.model;
        this.confidenceThreshold = builder.confidenceThreshold;
        this.maxTokens = builder.maxTokens;
        this.temperature = builder.temperature;
        this.includeRecommendations = builder.includeRecommendations;
    }

    public String getModel() {
        return model;
    }

    public double getConfidenceThreshold() {
        return confidenceThreshold;
    }

    public int getMaxTokens() {
        return maxTokens;
    }

    public double getTemperature() {
        return temperature;
    }

    public boolean isIncludeRecommendations() {
        return includeRecommendations;
    }

    public static class Builder {
        private String model = "gpt-4";
        private double confidenceThreshold = 0.8;
        private int maxTokens = 4000;
        private double temperature = 0.3;
        private boolean includeRecommendations = true;

        public Builder model(String model) {
            this.model = model;
            return this;
        }

        public Builder confidenceThreshold(double confidenceThreshold) {
            this.confidenceThreshold = confidenceThreshold;
            return this;
        }

        public Builder maxTokens(int maxTokens) {
            this.maxTokens = maxTokens;
            return this;
        }

        public Builder temperature(double temperature) {
            this.temperature = temperature;
            return this;
        }

        public Builder includeRecommendations(boolean includeRecommendations) {
            this.includeRecommendations = includeRecommendations;
            return this;
        }

        public AnalysisParameters build() {
            return new AnalysisParameters(this);
        }
    }

    public static Builder builder() {
        return new Builder();
    }
} 