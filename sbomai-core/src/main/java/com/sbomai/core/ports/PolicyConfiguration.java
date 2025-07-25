package com.sbomai.core.ports;

import java.util.Map;

/**
 * Configuration for policy enforcement.
 */
public class PolicyConfiguration {
    private final String name;
    private final String version;
    private final Map<String, Object> settings;
    private final String[] enabledPolicies;
    private final boolean isStrictMode;

    public PolicyConfiguration(String name, String version, Map<String, Object> settings, String[] enabledPolicies, boolean isStrictMode) {
        this.name = name;
        this.version = version;
        this.settings = settings;
        this.enabledPolicies = enabledPolicies;
        this.isStrictMode = isStrictMode;
    }

    public String getName() {
        return name;
    }

    public String getVersion() {
        return version;
    }

    public Map<String, Object> getSettings() {
        return settings;
    }

    public String[] getEnabledPolicies() {
        return enabledPolicies;
    }

    public boolean isStrictMode() {
        return isStrictMode;
    }

    public Object getSetting(String key) {
        return settings.get(key);
    }

    public Object getSetting(String key, Object defaultValue) {
        return settings.getOrDefault(key, defaultValue);
    }

    @Override
    public String toString() {
        return "PolicyConfiguration{" +
                "name='" + name + '\'' +
                ", version='" + version + '\'' +
                ", enabledPolicies=" + enabledPolicies.length +
                ", isStrictMode=" + isStrictMode +
                '}';
    }
} 