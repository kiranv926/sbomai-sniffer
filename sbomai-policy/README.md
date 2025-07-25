# SBOMAI Policy Enforcer Module

## Overview

The SBOMAI Policy Enforcer module is responsible for enforcing policies on SBOM components to ensure compliance with organizational standards. This module provides flexible policy enforcement capabilities for security, licensing, component, and custom policies.

## Features

- **Multi-policy Support**: License, security, component, version, supplier, and custom policies
- **Flexible Configuration**: Dynamic policy configuration and updates
- **Severity Classification**: Critical, high, medium, low, and info severity levels
- **Blocking Violations**: Support for blocking and non-blocking policy violations
- **Remediation Guidance**: Automatic remediation suggestions for violations
- **Policy Validation**: Component validation against all enabled policies
- **Extensible Framework**: Easy to add new policy types and rules

## Supported Policy Types

### License Policies
- **License Compliance**: Check for approved/disapproved licenses
- **License Compatibility**: Verify license compatibility with project
- **License Attribution**: Ensure proper license attribution
- **License Documentation**: Validate license documentation requirements

### Security Policies
- **CVSS Thresholds**: Enforce maximum CVSS scores
- **Vulnerability Age**: Check vulnerability disclosure age
- **Patch Availability**: Verify patch availability for vulnerabilities
- **Security Scanning**: Require security scanning results

### Component Policies
- **Component Approval**: Check component approval status
- **Component Age**: Enforce maximum component age
- **Component Source**: Validate component sources
- **Component Documentation**: Require component documentation

### Version Policies
- **Version Stability**: Prefer stable versions over pre-releases
- **Version Recency**: Enforce minimum version age
- **Version Compatibility**: Check version compatibility
- **Version Support**: Verify ongoing support for versions

### Supplier Policies
- **Supplier Approval**: Check supplier approval status
- **Supplier Reputation**: Validate supplier reputation
- **Supplier Support**: Verify supplier support availability
- **Supplier Compliance**: Check supplier compliance status

### Custom Policies
- **User-defined Rules**: Support for custom policy rules
- **Script-based Policies**: Execute custom scripts for validation
- **External Integrations**: Integrate with external policy systems
- **Conditional Logic**: Support for complex conditional policies

## Architecture

The policy enforcer module follows clean architecture principles:

```
src/main/java/com/sbomai/policy/
├── domain/           # Domain models and entities
│   ├── PolicyViolation.java
│   ├── PolicyType.java
│   └── Severity.java
├── ports/            # Interface contracts
│   ├── PolicyEnforcer.java
│   ├── PolicyEnforcementException.java
│   └── PolicyConfiguration.java
└── SbomaiPolicyApplication.java
```

## Quick Start

### Prerequisites
- Java 21+
- Maven 3.6+

### Building the Module
```bash
mvn clean install
```

### Running the Module
```bash
mvn spring-boot:run
```

## Usage

### Basic Policy Enforcement
```java
@Autowired
private PolicyEnforcer policyEnforcer;

// Prepare component data
Map<String, Object> componentData = new HashMap<>();
componentData.put("name", "log4j-core");
componentData.put("version", "2.14.1");
componentData.put("license", "Apache-2.0");
componentData.put("cvssScore", 9.8);
componentData.put("supplier", "Apache Software Foundation");

// Enforce all policies
List<PolicyViolation> violations = policyEnforcer.enforcePolicies(componentData);

// Check for blocking violations
boolean hasBlockingViolations = violations.stream()
    .anyMatch(PolicyViolation::isBlocking);
```

### Specific Policy Enforcement
```java
// Enforce license policies only
List<PolicyViolation> licenseViolations = policyEnforcer.enforcePolicy(
    componentData, PolicyType.LICENSE);

// Enforce specific policy by name
List<PolicyViolation> violations = policyEnforcer.enforcePolicyByName(
    componentData, "max-cvss-score");
```

### Policy Validation
```java
// Validate component without enforcing
boolean passesAllPolicies = policyEnforcer.validateComponent(componentData);

if (!passesAllPolicies) {
    // Component failed policy validation
    System.out.println("Component failed policy validation");
}
```

### Policy Configuration
```java
// Get current configuration
PolicyConfiguration config = policyEnforcer.getPolicyConfiguration();
System.out.println("Strict mode: " + config.isStrictMode());
System.out.println("Enabled policies: " + config.getEnabledPolicies());

// Update configuration
List<String> enabledPolicies = Arrays.asList("max-cvss-score", "license-compliance");
PolicyConfiguration newConfig = new PolicyConfiguration(
    enabledPolicies, true, new HashMap<>(), true, 10);
policyEnforcer.updatePolicyConfiguration(newConfig);
```

### Policy Management
```java
// Get available policies
List<String> availablePolicies = policyEnforcer.getAvailablePolicies();

// Check if policy is enabled
boolean isEnabled = policyEnforcer.isPolicyEnabled("max-cvss-score");

// Enable/disable policy
policyEnforcer.setPolicyEnabled("max-cvss-score", true);
```

## Configuration

### Application Properties
```yaml
# Policy Enforcer Configuration
sbomai:
  policy:
    # Policy Configuration
    policies:
      # License Policies
      license-compliance:
        enabled: true
        severity: HIGH
        blocking: true
        settings:
          allowed-licenses:
            - "Apache-2.0"
            - "MIT"
            - "BSD-3-Clause"
          disallowed-licenses:
            - "GPL-3.0"
            - "AGPL-3.0"
      
      # Security Policies
      max-cvss-score:
        enabled: true
        severity: CRITICAL
        blocking: true
        settings:
          max-score: 7.0
          include-pending: false
      
      # Component Policies
      component-age:
        enabled: true
        severity: MEDIUM
        blocking: false
        settings:
          max-age-days: 365
          exclude-stable: true
      
      # Version Policies
      version-stability:
        enabled: true
        severity: LOW
        blocking: false
        settings:
          prefer-stable: true
          allow-preleases: false
    
    # Enforcement Configuration
    enforcement:
      # Strict mode (fail on any violation)
      strict-mode: false
      
      # Fail on blocking violations
      fail-on-blocking: true
      
      # Maximum violations per component
      max-violations-per-component: 10
      
      # Include remediation suggestions
      include-remediation: true
      
      # Policy evaluation timeout (in milliseconds)
      timeout: 30000
```

### Policy Definition Files
```yaml
# policies/license-compliance.yml
name: "license-compliance"
type: "LICENSE"
severity: "HIGH"
blocking: true
description: "Enforce license compliance requirements"
rules:
  - name: "allowed-licenses"
    condition: "license in allowed_licenses"
    message: "License {license} is not in the allowed list"
    remediation: "Use one of the approved licenses: {allowed_licenses}"
  - name: "disallowed-licenses"
    condition: "license not in disallowed_licenses"
    message: "License {license} is explicitly disallowed"
    remediation: "Replace with an approved license"
settings:
  allowed_licenses:
    - "Apache-2.0"
    - "MIT"
    - "BSD-3-Clause"
  disallowed_licenses:
    - "GPL-3.0"
    - "AGPL-3.0"
```

## API Reference

### PolicyEnforcer Interface

#### Core Methods
- `enforcePolicies(Map<String, Object>)`: Enforce all policies
- `enforcePolicy(Map<String, Object>, PolicyType)`: Enforce specific policy type
- `enforcePolicyByName(Map<String, Object>, String)`: Enforce specific policy

#### Utility Methods
- `validateComponent(Map<String, Object>)`: Validate without enforcing
- `getPolicyConfiguration()`: Get current configuration
- `updatePolicyConfiguration(PolicyConfiguration)`: Update configuration
- `getAvailablePolicies()`: Get available policies
- `isPolicyEnabled(String)`: Check if policy is enabled
- `setPolicyEnabled(String, boolean)`: Enable/disable policy

### Domain Models

#### PolicyViolation
Represents a policy violation with:
- Policy name and type
- Severity level
- Component information
- Blocking status
- Detection timestamp
- Details and remediation

#### PolicyType
Enumeration of policy types:
- `LICENSE`: License compliance policies
- `SECURITY`: Security-related policies
- `COMPONENT`: Component-specific policies
- `VERSION`: Version-related policies
- `SUPPLIER`: Supplier-related policies
- `CUSTOM`: Custom user-defined policies

#### Severity
Enumeration of violation severity levels:
- `CRITICAL`: Critical violations
- `HIGH`: High severity violations
- `MEDIUM`: Medium severity violations
- `LOW`: Low severity violations
- `INFO`: Informational violations

## Error Handling

### PolicyEnforcementException
Thrown when policy enforcement fails:
```java
try {
    List<PolicyViolation> violations = policyEnforcer.enforcePolicies(componentData);
} catch (PolicyEnforcementException e) {
    logger.error("Policy enforcement failed: {}", e.getMessage());
}
```

### Common Error Scenarios
- Invalid policy configuration
- Missing required component data
- Policy evaluation timeout
- External policy system failures
- Configuration update errors

## Policy Development

### Creating Custom Policies

1. **Define Policy Structure**
```java
@Component
public class CustomPolicy implements Policy {
    @Override
    public List<PolicyViolation> evaluate(Map<String, Object> componentData) {
        // Implement policy logic
        List<PolicyViolation> violations = new ArrayList<>();
        
        // Check custom conditions
        if (customCondition(componentData)) {
            violations.add(new PolicyViolation(
                "custom-policy", PolicyType.CUSTOM, Severity.MEDIUM, 
                "Custom policy violation"));
        }
        
        return violations;
    }
}
```

2. **Register Policy**
```java
@Configuration
public class PolicyConfig {
    @Bean
    public Policy customPolicy() {
        return new CustomPolicy();
    }
}
```

3. **Configure Policy**
```yaml
sbomai:
  policy:
    policies:
      custom-policy:
        enabled: true
        severity: MEDIUM
        blocking: false
        settings:
          custom-setting: "value"
```

### Policy Templates

#### License Policy Template
```yaml
name: "license-policy-template"
type: "LICENSE"
rules:
  - name: "license-approval"
    condition: "license in approved_licenses"
    message: "License {license} requires approval"
    remediation: "Contact legal team for license approval"
```

#### Security Policy Template
```yaml
name: "security-policy-template"
type: "SECURITY"
rules:
  - name: "cvss-threshold"
    condition: "cvss_score <= max_cvss_score"
    message: "CVSS score {cvss_score} exceeds threshold {max_cvss_score}"
    remediation: "Update to a version with lower CVSS score"
```

## Integration

### With Other SBOMAI Modules
The policy enforcer integrates with:

- **Parser Module**: Uses parsed component information
- **Vulnerability Scanner**: Uses vulnerability data for security policies
- **Core Module**: Provides policy enforcement for analysis
- **CLI Module**: Enables policy checking from command line

### External Integration
```java
// Spring Boot integration
@Autowired
private PolicyEnforcer policyEnforcer;

// Direct instantiation
PolicyEnforcer enforcer = new DefaultPolicyEnforcer();
```

## Performance Optimization

### Caching Strategy
- Cache policy evaluation results
- Cache policy configurations
- Memory-efficient caching implementation

### Parallel Processing
- Parallel policy evaluation for multiple components
- Configurable concurrency limits
- Non-blocking operations

### Optimization Tips
- Use efficient data structures for policy rules
- Implement early termination for blocking violations
- Optimize policy condition evaluation

## Monitoring and Metrics

### Policy Metrics
- Policy evaluation counts
- Violation rates by policy type
- Policy evaluation duration
- Configuration change tracking

### Health Checks
```java
// Check policy enforcer health
PolicyConfiguration config = policyEnforcer.getPolicyConfiguration();
boolean healthy = config != null && !config.getEnabledPolicies().isEmpty();
```

## Troubleshooting

### Common Issues

1. **Policy Configuration Errors**
   - Validate policy configuration syntax
   - Check policy file permissions
   - Verify policy dependencies

2. **Performance Issues**
   - Optimize policy evaluation logic
   - Implement caching for repeated evaluations
   - Use parallel processing for multiple components

3. **Integration Problems**
   - Verify component data format
   - Check policy enforcer availability
   - Review integration configuration

### Debug Mode
Enable debug logging:
```yaml
logging:
  level:
    com.sbomai.policy: DEBUG
```

## Security Considerations

### Policy Security
- Validate policy configurations
- Sanitize policy inputs
- Implement policy access controls
- Audit policy changes

### Data Privacy
- Minimize data retention
- Secure policy data transmission
- Implement access controls
- Audit policy evaluations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests for new functionality
5. Submit a pull request

### Adding New Policy Types

1. **Create Policy Type**
```java
public enum PolicyType {
    // ... existing types
    NEW_TYPE("New Type", "Description of new policy type");
}
```

2. **Implement Policy Logic**
```java
@Component
public class NewTypePolicy implements Policy {
    // Implement policy evaluation logic
}
```

3. **Add Configuration Support**
```yaml
sbomai:
  policy:
    policies:
      new-type-policy:
        enabled: true
        severity: MEDIUM
        blocking: false
```

## License

This module is part of the SBOMAI project and is licensed under the same terms as the main project.

## Support

For issues and questions:
- Create an issue in the project repository
- Check the documentation
- Review existing issues for solutions 