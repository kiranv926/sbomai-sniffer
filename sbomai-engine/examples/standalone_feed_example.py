"""
Standalone example of enhanced vulnerability feed analysis.
"""

import asyncio
import json
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from pprint import pprint

@dataclass
class ThreatIntelData:
    """Threat intelligence data for a vulnerability"""
    active_exploitation: bool = False
    threat_actors: List[str] = field(default_factory=list)
    malware_families: List[str] = field(default_factory=list)
    targeted_industries: List[str] = field(default_factory=list)
    exploit_urls: List[str] = field(default_factory=list)
    trending_score: float = 0.0
    last_seen: Optional[datetime] = None

@dataclass
class EnhancedVulnerabilityInfo:
    """Enhanced vulnerability information with threat intel"""
    cve_id: str
    description: str
    cvss_base_score: float
    cvss_temporal_score: float
    cvss_environmental_score: float
    cvss_vector: str
    severity: str
    affected_purls: List[str]
    affected_cpes: List[str]
    references: List[str]
    exploit_status: str
    published_date: datetime
    last_modified_date: datetime
    fixed_versions: List[str]
    ecosystem: str
    threat_intel: ThreatIntelData = field(default_factory=ThreatIntelData)
    os_patches: Dict[str, str] = field(default_factory=dict)
    detailed_analysis: Dict[str, str] = field(default_factory=dict)
    emerging_threat: bool = False

# Example SBOM with known vulnerable components
TEST_SBOM = {
    "bomFormat": "CycloneDX",
    "specVersion": "1.4",
    "components": [
        {
            "type": "library",
            "name": "log4j-core",
            "version": "2.14.1",
            "purl": "pkg:maven/org.apache.logging.log4j/log4j-core@2.14.1"
        },
        {
            "type": "library",
            "name": "spring-core",
            "version": "5.3.13",
            "purl": "pkg:maven/org.springframework/spring-core@5.3.13"
        }
    ]
}

# Simulated vulnerability data from different sources
SAMPLE_VULNERABILITY_DATA = {
    "CVE-2021-44228": {  # Log4Shell
        "nvd": {
            "description": "Apache Log4j2 2.0-beta9 through 2.15.0 JNDI features used in configuration, log messages, and parameters do not protect against attacker-controlled LDAP and other JNDI related endpoints. An attacker who can control log messages or log message parameters can execute arbitrary code loaded from LDAP servers when message lookup substitution is enabled.",
            "cvss_score": 10.0,
            "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H"
        },
        "exploit_db": {
            "exploit_count": 5,
            "latest_exploit": "2021-12-10",
            "exploit_urls": [
                "https://www.exploit-db.com/exploits/50590",
                "https://www.exploit-db.com/exploits/50592"
            ]
        },
        "os_patches": {
            "redhat": "RHSA-2021:4904",
            "ubuntu": "USN-5192-1",
            "alpine": "CVE-2021-44228-r0"
        },
        "threat_intel": {
            "active_exploitation": True,
            "threat_actors": ["APT41", "Hafnium", "PHOSPHORUS"],
            "malware_families": ["Khonsari", "Muhstik", "Mirai"],
            "targeted_industries": ["Technology", "Financial Services", "Government"],
            "trending_score": 9.8
        },
        "detailed_analysis": {
            "root_cause": "JNDI lookup feature in Log4j allows remote code execution",
            "affected_functions": ["org.apache.logging.log4j.core.lookup.JndiLookup"],
            "attack_vectors": [
                "LDAP injection",
                "JNDI manipulation",
                "Remote class loading"
            ]
        }
    },
    "CVE-2022-22965": {  # Spring4Shell
        "nvd": {
            "description": "A Spring MVC or Spring WebFlux application running on JDK 9+ may be vulnerable to remote code execution (RCE) via data binding. The specific exploit requires the application to run on Tomcat as a WAR deployment. If the application is deployed as a Spring Boot executable jar, i.e. the default, it is not vulnerable to the exploit.",
            "cvss_score": 9.8,
            "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"
        },
        "exploit_db": {
            "exploit_count": 2,
            "latest_exploit": "2022-04-01",
            "exploit_urls": [
                "https://www.exploit-db.com/exploits/50688"
            ]
        },
        "os_patches": {
            "redhat": "RHSA-2022:1461",
            "ubuntu": "USN-5376-1"
        },
        "threat_intel": {
            "active_exploitation": True,
            "threat_actors": ["DEV-0401", "TAG-22"],
            "malware_families": ["WebShell", "Mirai"],
            "targeted_industries": ["Government", "Education", "Healthcare"],
            "trending_score": 8.5
        },
        "detailed_analysis": {
            "root_cause": "Class property binding vulnerability in Spring Core",
            "affected_functions": ["org.springframework.beans.BeanWrapperImpl"],
            "attack_vectors": [
                "Class property manipulation",
                "Request parameter injection"
            ]
        }
    }
}

def create_sample_vulnerability(cve_id: str, data: dict) -> EnhancedVulnerabilityInfo:
    """Create a sample vulnerability with enhanced data"""
    nvd = data["nvd"]
    exploit = data["exploit_db"]
    threat = data["threat_intel"]
    
    return EnhancedVulnerabilityInfo(
        cve_id=cve_id,
        description=nvd["description"],
        cvss_base_score=nvd["cvss_score"],
        cvss_temporal_score=nvd["cvss_score"],
        cvss_environmental_score=nvd["cvss_score"],
        cvss_vector=nvd["cvss_vector"],
        severity="CRITICAL",
        affected_purls=[],
        affected_cpes=[],
        references=exploit["exploit_urls"],
        exploit_status="ACTIVELY_EXPLOITED" if threat["active_exploitation"] else "PROOF_OF_CONCEPT",
        published_date=datetime.now(),
        last_modified_date=datetime.now(),
        fixed_versions=[],
        ecosystem="maven",
        threat_intel=ThreatIntelData(
            active_exploitation=threat["active_exploitation"],
            threat_actors=threat["threat_actors"],
            malware_families=threat["malware_families"],
            targeted_industries=threat["targeted_industries"],
            trending_score=threat["trending_score"]
        ),
        os_patches=data["os_patches"],
        detailed_analysis=data["detailed_analysis"],
        emerging_threat=threat["trending_score"] > 8.0
    )

def calculate_risk_score(vuln: EnhancedVulnerabilityInfo) -> float:
    """Calculate enhanced risk score based on all signals"""
    # Base risk from CVSS
    base_risk = vuln.cvss_base_score / 10.0
    
    # Threat intelligence factors
    threat_score = 0.0
    if vuln.threat_intel.active_exploitation:
        threat_score += 0.3
    threat_score += min(len(vuln.threat_intel.threat_actors) * 0.1, 0.3)
    threat_score += min(len(vuln.threat_intel.malware_families) * 0.1, 0.2)
    
    # Exploit availability
    exploit_score = 0.0
    if vuln.exploit_status == "ACTIVELY_EXPLOITED":
        exploit_score = 0.3
    elif vuln.exploit_status == "PROOF_OF_CONCEPT":
        exploit_score = 0.2
    
    # Trending factor
    trending_score = vuln.threat_intel.trending_score / 10.0 * 0.2
    
    # Combine scores
    total_score = base_risk * (1 + threat_score + exploit_score + trending_score)
    return min(total_score * 10, 10.0)  # Cap at 10.0

def print_vulnerability_analysis(vuln: EnhancedVulnerabilityInfo):
    """Print detailed vulnerability analysis with enhanced data"""
    print("\n" + "="*80)
    print(f"Vulnerability Analysis: {vuln.cve_id}")
    print("="*80)
    
    # Basic Info
    print("\nBasic Information:")
    print(f"Description: {vuln.description[:200]}...")
    print(f"CVSS Base Score: {vuln.cvss_base_score}")
    print(f"CVSS Vector: {vuln.cvss_vector}")
    print(f"Exploit Status: {vuln.exploit_status}")
    
    # Threat Intelligence
    print("\nThreat Intelligence:")
    print(f"Active Exploitation: {vuln.threat_intel.active_exploitation}")
    if vuln.threat_intel.threat_actors:
        print("Known Threat Actors:")
        for actor in vuln.threat_intel.threat_actors:
            print(f"- {actor}")
    
    if vuln.threat_intel.malware_families:
        print("\nAssociated Malware:")
        for malware in vuln.threat_intel.malware_families:
            print(f"- {malware}")
    
    if vuln.threat_intel.targeted_industries:
        print("\nTargeted Industries:")
        for industry in vuln.threat_intel.targeted_industries:
            print(f"- {industry}")
    
    print(f"\nTrending Score: {vuln.threat_intel.trending_score}/10.0")
    
    # Technical Details
    print("\nTechnical Analysis:")
    if "root_cause" in vuln.detailed_analysis:
        print(f"Root Cause: {vuln.detailed_analysis['root_cause']}")
    
    if "affected_functions" in vuln.detailed_analysis:
        print("\nAffected Functions:")
        for func in vuln.detailed_analysis['affected_functions']:
            print(f"- {func}")
    
    if "attack_vectors" in vuln.detailed_analysis:
        print("\nAttack Vectors:")
        for vector in vuln.detailed_analysis['attack_vectors']:
            print(f"- {vector}")
    
    # Available Patches
    print("\nAvailable Patches:")
    for os_name, patch in vuln.os_patches.items():
        print(f"- {os_name}: {patch}")
    
    # Exploit References
    if vuln.references:
        print("\nKnown Exploits:")
        for ref in vuln.references:
            print(f"- {ref}")
    
    # Enhanced Risk Assessment
    risk_score = calculate_risk_score(vuln)
    print("\nEnhanced Risk Assessment:")
    print(f"Final Risk Score: {risk_score:.1f}/10.0")
    
    risk_factors = []
    if vuln.threat_intel.active_exploitation:
        risk_factors.append("Active exploitation detected in the wild")
    if len(vuln.threat_intel.threat_actors) > 2:
        risk_factors.append("Multiple threat actors involved")
    if vuln.threat_intel.trending_score > 8.0:
        risk_factors.append("Highly trending vulnerability")
    if len(vuln.references) > 1:
        risk_factors.append("Multiple public exploits available")
    
    if risk_factors:
        print("\nKey Risk Factors:")
        for factor in risk_factors:
            print(f"- {factor}")
    
    # Recommendations
    print("\nRecommendations:")
    if risk_score >= 8.0:
        print("- CRITICAL: Immediate patching required")
        print("- Implement detection rules for exploitation attempts")
        print("- Monitor for indicators of compromise")
    elif risk_score >= 6.0:
        print("- HIGH: Prioritize patching within 24-48 hours")
        print("- Review application logs for suspicious activity")
    else:
        print("- Schedule patching according to regular maintenance windows")
        print("- Monitor for changes in exploitation status")

def analyze_sbom():
    """Analyze SBOM with enhanced vulnerability data"""
    print("\n=== Enhanced SBOM Security Analysis ===\n")
    
    # Create vulnerability database
    vuln_db = {
        cve_id: create_sample_vulnerability(cve_id, data)
        for cve_id, data in SAMPLE_VULNERABILITY_DATA.items()
    }
    
    # Analyze each component
    for component in TEST_SBOM["components"]:
        print(f"\nAnalyzing component: {component['name']} {component['version']}")
        print(f"Package URL: {component['purl']}")
        
        # Find relevant vulnerabilities
        if "log4j" in component["name"] and component["version"].startswith("2.14"):
            vuln = vuln_db["CVE-2021-44228"]
            print_vulnerability_analysis(vuln)
        
        elif "spring-core" in component["name"] and component["version"].startswith("5.3"):
            vuln = vuln_db["CVE-2022-22965"]
            print_vulnerability_analysis(vuln)

if __name__ == "__main__":
    analyze_sbom()