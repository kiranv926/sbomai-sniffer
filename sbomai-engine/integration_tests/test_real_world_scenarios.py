"""
Integration tests demonstrating real-world SBOM analysis scenarios.
"""

import json
import datetime
from pprint import pprint

# Test Scenarios
SPRING_BOOT_SBOM = {
    "bomFormat": "CycloneDX",
    "specVersion": "1.4",
    "metadata": {
        "timestamp": "2024-03-15T10:00:00Z",
        "tools": [
            {
                "vendor": "Example Corp",
                "name": "sbom-generator",
                "version": "1.0.0"
            }
        ],
        "component": {
            "type": "application",
            "name": "spring-boot-app",
            "version": "1.0.0"
        }
    },
    "components": [
        {
            "type": "library",
            "name": "spring-boot-starter-web",
            "version": "2.6.1",
            "purl": "pkg:maven/org.springframework.boot/spring-boot-starter-web@2.6.1"
        },
        {
            "type": "library",
            "name": "spring-web",
            "version": "5.3.13",
            "purl": "pkg:maven/org.springframework/spring-web@5.3.13"
        },
        {
            "type": "library",
            "name": "log4j-core",
            "version": "2.14.1",
            "purl": "pkg:maven/org.apache.logging.log4j/log4j-core@2.14.1"
        }
    ]
}

NODE_APP_SBOM = {
    "bomFormat": "CycloneDX",
    "specVersion": "1.4",
    "metadata": {
        "timestamp": "2024-03-15T10:00:00Z",
        "component": {
            "type": "application",
            "name": "node-express-app",
            "version": "1.0.0"
        }
    },
    "components": [
        {
            "type": "library",
            "name": "express",
            "version": "4.17.1",
            "purl": "pkg:npm/express@4.17.1"
        },
        {
            "type": "library",
            "name": "lodash",
            "version": "4.17.15",
            "purl": "pkg:npm/lodash@4.17.15"
        },
        {
            "type": "library",
            "name": "minimist",
            "version": "1.2.5",
            "purl": "pkg:npm/minimist@1.2.5"
        }
    ]
}

PYTHON_APP_SBOM = {
    "bomFormat": "CycloneDX",
    "specVersion": "1.4",
    "metadata": {
        "timestamp": "2024-03-15T10:00:00Z",
        "component": {
            "type": "application",
            "name": "flask-ml-app",
            "version": "1.0.0"
        }
    },
    "components": [
        {
            "type": "library",
            "name": "flask",
            "version": "2.0.1",
            "purl": "pkg:pypi/flask@2.0.1"
        },
        {
            "type": "library",
            "name": "numpy",
            "version": "1.21.0",
            "purl": "pkg:pypi/numpy@1.21.0"
        },
        {
            "type": "library",
            "name": "tensorflow",
            "version": "2.7.0",
            "purl": "pkg:pypi/tensorflow@2.7.0"
        }
    ]
}

class VulnerabilityIntelligence:
    """Mock of the VulnerabilityIntelligence class for demonstration"""
    
    def __init__(self):
        self.vulnerability_db = {
            "pkg:maven/org.apache.logging.log4j/log4j-core@2.14.1": {
                "cve_id": "CVE-2021-44228",
                "severity": "CRITICAL",
                "cvss_score": 10.0,
                "description": "Remote code execution vulnerability in Log4j",
                "exploit_status": "ACTIVELY_EXPLOITED",
                "remediation": "Upgrade to version 2.15.0 or higher"
            },
            "pkg:maven/org.springframework/spring-web@5.3.13": {
                "cve_id": "CVE-2022-22965",
                "severity": "CRITICAL",
                "cvss_score": 9.8,
                "description": "Spring4Shell RCE vulnerability",
                "exploit_status": "PROOF_OF_CONCEPT",
                "remediation": "Upgrade to version 5.3.18 or higher"
            },
            "pkg:npm/lodash@4.17.15": {
                "cve_id": "CVE-2020-8203",
                "severity": "HIGH",
                "cvss_score": 7.4,
                "description": "Prototype pollution vulnerability",
                "exploit_status": "PROOF_OF_CONCEPT",
                "remediation": "Upgrade to version 4.17.19 or higher"
            },
            "pkg:pypi/tensorflow@2.7.0": {
                "cve_id": "CVE-2022-29216",
                "severity": "HIGH",
                "cvss_score": 7.8,
                "description": "Heap buffer overflow in TensorFlow",
                "exploit_status": "UNPROVEN",
                "remediation": "Upgrade to version 2.7.1 or higher"
            }
        }
    
    def analyze_component(self, purl):
        """Analyze a single component"""
        if purl in self.vulnerability_db:
            vuln = self.vulnerability_db[purl]
            return {
                "has_vulnerabilities": True,
                "highest_severity": vuln["severity"],
                "highest_cvss": vuln["cvss_score"],
                "vulnerabilities": [vuln],
                "risk_score": self._calculate_risk_score(vuln)
            }
        return {
            "has_vulnerabilities": False,
            "highest_severity": "NONE",
            "highest_cvss": 0.0,
            "vulnerabilities": [],
            "risk_score": 0.0
        }
    
    def _calculate_risk_score(self, vuln):
        """Calculate risk score based on CVSS and exploit status"""
        exploit_weights = {
            "ACTIVELY_EXPLOITED": 1.0,
            "PROOF_OF_CONCEPT": 0.7,
            "UNPROVEN": 0.4
        }
        base_score = vuln["cvss_score"] / 10.0
        exploit_factor = exploit_weights.get(vuln["exploit_status"], 0.1)
        return round(base_score * exploit_factor * 10, 1)

class DependencyAnalyzer:
    """Mock of the DependencyAnalyzer class for demonstration"""
    
    def analyze_dependencies(self, sbom):
        """Analyze dependencies in SBOM"""
        vuln_intel = VulnerabilityIntelligence()
        results = {
            "total_components": len(sbom["components"]),
            "vulnerable_components": 0,
            "risk_scores": [],
            "critical_components": [],
            "high_risk_paths": []
        }
        
        # Analyze each component
        for component in sbom["components"]:
            analysis = vuln_intel.analyze_component(component["purl"])
            if analysis["has_vulnerabilities"]:
                results["vulnerable_components"] += 1
                results["risk_scores"].append(analysis["risk_score"])
                
                if analysis["highest_severity"] in ["CRITICAL", "HIGH"]:
                    results["critical_components"].append({
                        "component": f"{component['name']}@{component['version']}",
                        "analysis": analysis
                    })
                    
                    # Add risk path
                    results["high_risk_paths"].append({
                        "path": [
                            sbom["metadata"]["component"]["name"],
                            f"{component['name']}@{component['version']}"
                        ],
                        "risk_score": analysis["risk_score"],
                        "vulnerabilities": analysis["vulnerabilities"]
                    })
        
        # Calculate overall metrics
        results["average_risk_score"] = (
            round(sum(results["risk_scores"]) / len(results["risk_scores"]), 1)
            if results["risk_scores"] else 0.0
        )
        results["risk_status"] = self._determine_risk_status(results["average_risk_score"])
        
        return results
    
    def _determine_risk_status(self, risk_score):
        """Determine overall risk status"""
        if risk_score >= 8.0:
            return "CRITICAL"
        elif risk_score >= 6.0:
            return "HIGH"
        elif risk_score >= 4.0:
            return "MEDIUM"
        elif risk_score > 0:
            return "LOW"
        return "NONE"

def analyze_sbom(sbom_data):
    """Analyze SBOM and generate comprehensive report"""
    print(f"\n=== Analyzing {sbom_data['metadata']['component']['name']} ===")
    print(f"Version: {sbom_data['metadata']['component']['version']}")
    print(f"Format: {sbom_data['bomFormat']} {sbom_data['specVersion']}")
    print(f"Generated: {sbom_data['metadata']['timestamp']}")
    
    # Analyze dependencies
    analyzer = DependencyAnalyzer()
    results = analyzer.analyze_dependencies(sbom_data)
    
    # Print summary
    print("\nSummary:")
    print(f"Total Components: {results['total_components']}")
    print(f"Vulnerable Components: {results['vulnerable_components']}")
    print(f"Average Risk Score: {results['average_risk_score']}")
    print(f"Risk Status: {results['risk_status']}")
    
    # Print critical components
    if results["critical_components"]:
        print("\nCritical Components:")
        for comp in results["critical_components"]:
            print(f"\n- {comp['component']}")
            for vuln in comp['analysis']['vulnerabilities']:
                print(f"  CVE: {vuln['cve_id']}")
                print(f"  Severity: {vuln['severity']}")
                print(f"  CVSS: {vuln['cvss_score']}")
                print(f"  Description: {vuln['description']}")
                print(f"  Remediation: {vuln['remediation']}")
    
    # Print risk paths
    if results["high_risk_paths"]:
        print("\nHigh Risk Paths:")
        for path in results["high_risk_paths"]:
            print(f"\n- Path: {' → '.join(path['path'])}")
            print(f"  Risk Score: {path['risk_score']}")
            for vuln in path['vulnerabilities']:
                print(f"  Vulnerability: {vuln['cve_id']} ({vuln['severity']})")

def main():
    """Run analysis on all example SBOMs"""
    
    print("\n=== SBOMAI Engine Integration Test ===")
    print("Running real-world scenario analysis...")
    
    # Analyze Spring Boot application
    print("\n\n=== Spring Boot Application Analysis ===")
    analyze_sbom(SPRING_BOOT_SBOM)
    
    # Analyze Node.js application
    print("\n\n=== Node.js Application Analysis ===")
    analyze_sbom(NODE_APP_SBOM)
    
    # Analyze Python application
    print("\n\n=== Python Application Analysis ===")
    analyze_sbom(PYTHON_APP_SBOM)

if __name__ == "__main__":
    main()