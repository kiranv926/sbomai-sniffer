package com.sbomai.core.ports;

/**
 * Cost estimate for AI analysis operations.
 */
public class CostEstimate {
    private final double estimatedCost;
    private final String currency;
    private final String model;
    private final int estimatedTokens;
    private final String costBreakdown;

    public CostEstimate(double estimatedCost, String currency, String model, int estimatedTokens, String costBreakdown) {
        this.estimatedCost = estimatedCost;
        this.currency = currency;
        this.model = model;
        this.estimatedTokens = estimatedTokens;
        this.costBreakdown = costBreakdown;
    }

    public double getEstimatedCost() {
        return estimatedCost;
    }

    public String getCurrency() {
        return currency;
    }

    public String getModel() {
        return model;
    }

    public int getEstimatedTokens() {
        return estimatedTokens;
    }

    public String getCostBreakdown() {
        return costBreakdown;
    }

    @Override
    public String toString() {
        return "CostEstimate{" +
                "estimatedCost=" + estimatedCost +
                ", currency='" + currency + '\'' +
                ", model='" + model + '\'' +
                ", estimatedTokens=" + estimatedTokens +
                '}';
    }
} 