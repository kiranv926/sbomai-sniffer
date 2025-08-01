# SBOMAI Engine Model Architecture

## Core Models Overview

### 1. VulnerabilityIntelligence Model
```python
class VulnerabilityIntelligence:
    """
    Primary model for vulnerability analysis and risk assessment.
    Currently implemented as a rule-based system with the following components:
    
    - Vulnerability Database: In-memory store of known vulnerabilities
    - Risk Scoring Engine: CVSS-based scoring with exploit status weighting
    - Component Analysis: Individual package vulnerability assessment
    """
    
    Risk Scoring Formula:
    final_risk_score = (base_cvss_score / 10.0) * exploit_status_weight * 10
    
    Exploit Status Weights:
    - ACTIVELY_EXPLOITED: 1.0  (100% of base CVSS)
    - PROOF_OF_CONCEPT:   0.7  (70% of base CVSS)
    - UNPROVEN:          0.4  (40% of base CVSS)
```

### 2. DependencyAnalyzer Model
```python
class DependencyAnalyzer:
    """
    Analyzes dependency relationships and vulnerability propagation.
    Features:
    
    - Component Counting: Tracks total and vulnerable components
    - Risk Path Analysis: Identifies critical dependency chains
    - Risk Aggregation: Calculates overall project risk scores
    """
    
    Risk Status Thresholds:
    - CRITICAL: >= 8.0
    - HIGH:     >= 6.0
    - MEDIUM:   >= 4.0
    - LOW:      > 0.0
    - NONE:     = 0.0
```

## Model Selection Rationale

1. **Base Models**
   - Rule-based vulnerability matching
   - CVSS score normalization
   - Exploit status weighting
   - Dependency graph analysis

2. **Why These Models?**
   - Deterministic behavior for testing
   - Clear risk scoring logic
   - Traceable decision paths
   - Easy to validate outputs

3. **Production vs Test Models**
   The test implementation uses simplified versions of:
   - Vulnerability Database (in-memory vs. distributed database)
   - Risk Scoring (basic weights vs. ML-based scoring)
   - Dependency Analysis (direct paths vs. graph neural networks)

## Default Test Configuration

### 1. Vulnerability Database
```json
{
    "pkg:maven/org.apache.logging.log4j/log4j-core@2.14.1": {
        "cve_id": "CVE-2021-44228",
        "severity": "CRITICAL",
        "cvss_score": 10.0,
        "exploit_status": "ACTIVELY_EXPLOITED"
    },
    "pkg:maven/org.springframework/spring-web@5.3.13": {
        "cve_id": "CVE-2022-22965",
        "severity": "CRITICAL",
        "cvss_score": 9.8,
        "exploit_status": "PROOF_OF_CONCEPT"
    }
    // ... other vulnerabilities
}
```

### 2. Risk Scoring Matrix
```
Final Risk Score = Base CVSS * Exploit Weight

Example:
- Log4Shell (CVSS 10.0, Actively Exploited)
  10.0 * 1.0 = 10.0 (Critical Risk)
  
- Spring4Shell (CVSS 9.8, PoC Available)
  9.8 * 0.7 = 6.9 (High Risk)
```

### 3. Dependency Analysis Configuration
```python
{
    "metrics": {
        "total_components": int,
        "vulnerable_components": int,
        "risk_scores": List[float],
        "critical_components": List[Dict],
        "high_risk_paths": List[Dict]
    }
}
```

## Production Model Differences

1. **Advanced Models (Not in Test)**
   - Graph Neural Networks for dependency analysis
   - Machine Learning for exploit prediction
   - Natural Language Processing for vulnerability description analysis
   - Time-series analysis for vulnerability trend prediction

2. **Enhanced Features (Not in Test)**
   - Historical vulnerability pattern analysis
   - Code similarity scoring
   - Contributor behavior analysis
   - Supply chain risk propagation

3. **Additional Data Sources (Not in Test)**
   - Real-time CVE feeds
   - GitHub Security Advisories
   - ExploitDB integration
   - MITRE ATT&CK correlation

## Test Coverage

1. **Vulnerability Detection**
   - Known CVE matching
   - CVSS score interpretation
   - Severity classification
   - Exploit status assessment

2. **Risk Analysis**
   - Component-level scoring
   - Application-wide risk assessment
   - Critical path identification
   - Risk aggregation

3. **Dependency Analysis**
   - Direct dependency scanning
   - Vulnerability propagation
   - Component relationship mapping
   - Risk path visualization

## Model Limitations in Test Environment

1. **Simplified Scoring**
   - Uses basic multiplication instead of ML-based scoring
   - Limited exploit status categories
   - No temporal scoring factors

2. **Static Database**
   - Pre-defined vulnerability set
   - No real-time updates
   - Limited vulnerability metadata

3. **Basic Dependency Analysis**
   - Direct path analysis only
   - No transitive vulnerability calculation
   - Limited dependency graph depth

## Future Enhancements

1. **ML Model Integration**
   ```python
   class MLBasedScoring:
       """
       To be implemented:
       - Exploit prediction using historical data
       - Risk scoring using multiple factors
       - Pattern recognition in dependency chains
       """
   ```

2. **Graph Neural Networks**
   ```python
   class DependencyGNN:
       """
       To be implemented:
       - Node feature extraction
       - Edge weight calculation
       - Risk propagation analysis
       - Critical path prediction
       """
   ```

3. **Natural Language Processing**
   ```python
   class VulnerabilityNLP:
       """
       To be implemented:
       - Description similarity analysis
       - Exploit narrative understanding
       - Remediation recommendation generation
       - Impact assessment automation
       """
   ```