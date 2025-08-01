"""
Real-world example of enhanced vulnerability feed integration.
"""

import asyncio
import json
from datetime import datetime
from pprint import pprint

from src.sbomai_ai.feeds.enhanced_vulnerability_feed import (
    EnhancedVulnerabilityFeedManager,
    EnhancedVulnerabilityInfo,
    ThreatIntelData
)

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
            "description": "Apache Log4j2 2.0-beta9 through 2.15.0 JNDI features...",
            "cvss_score": 10.0,
            "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H"
        },
        "exploit_db": {
            "exploit_count": 5,
            "latest_exploit": "2021-12-10",
            "exploit_urls": [
                "https://www.exploit-db.com/exploits/50590"
            ]
        },
        "os_patches": {
            "redhat": "RHSA-2021:4904",
            "ubuntu": "USN-5192-1",
            "alpine": "CVE-2021-44228-r0"
        },
        "threat_intel": {
            "active_exploitation": True,
            "threat_actors": ["APT41", "Hafnium"],
            "malware_families": ["Khonsari", "Muhstik"],
            "targeted_industries": ["Technology", "Financial Services"],
            "trending_score": 9.8
        }
    },
    "CVE-2022-22965": {  # Spring4Shell
        "nvd": {
            "description": "A Spring MVC or Spring WebFlux application running on JDK 9+...",
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
            "threat_actors": ["DEV-0401"],
            "malware_families": ["WebShell"],
            "targeted_industries": ["Government", "Education"],
            "trending_score": 8.5
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
        affected_purls=[],  # Will be populated based on analysis
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
        detailed_analysis={},
        emerging_threat=threat["trending_score"] > 8.0
    )

async def analyze_sbom_with_enhanced_feeds():
    """Analyze SBOM using enhanced vulnerability feeds"""
    print("\n=== Enhanced Vulnerability Analysis ===\n")
    
    # Initialize feed manager
    config = {
        'update_interval': 3600,
        'nvd_api_key': 'test',
        'github_token': 'test',
        'snyk_api_key': 'test',
        'otx_api_key': 'test',
        'twitter_auth': {'bearer_token': 'test'}
    }
    feed_manager = EnhancedVulnerabilityFeedManager(config)
    
    # Populate with sample data
    for cve_id, data in SAMPLE_VULNERABILITY_DATA.items():
        vuln = create_sample_vulnerability(cve_id, data)
        feed_manager.vulnerability_db[cve_id] = vuln
    
    # Analyze SBOM components
    print("Analyzing SBOM components...")
    for component in TEST_SBOM["components"]:
        purl = component["purl"]
        name = component["name"]
        version = component["version"]
        
        print(f"\nComponent: {name} {version}")
        print(f"Package URL: {purl}")
        
        # Find relevant vulnerabilities
        if "log4j" in name and version.startswith("2.14"):
            cve = "CVE-2021-44228"
            vuln = feed_manager.get_vulnerability(cve)
            print_vulnerability_analysis(vuln)
        
        elif "spring-core" in name and version.startswith("5.3"):
            cve = "CVE-2022-22965"
            vuln = feed_manager.get_vulnerability(cve)
            print_vulnerability_analysis(vuln)

def print_vulnerability_analysis(vuln: EnhancedVulnerabilityInfo):
    """Print detailed vulnerability analysis"""
    print("\nVulnerability Analysis:")
    print(f"CVE ID: {vuln.cve_id}")
    print(f"Description: {vuln.description}")
    print(f"CVSS Base Score: {vuln.cvss_base_score}")
    print(f"CVSS Vector: {vuln.cvss_vector}")
    print(f"Exploit Status: {vuln.exploit_status}")
    
    # Threat Intelligence
    print("\nThreat Intelligence:")
    print(f"Active Exploitation: {vuln.threat_intel.active_exploitation}")
    print("Threat Actors:", ", ".join(vuln.threat_intel.threat_actors))
    print("Malware Families:", ", ".join(vuln.threat_intel.malware_families))
    print("Targeted Industries:", ", ".join(vuln.threat_intel.targeted_industries))
    print(f"Trending Score: {vuln.threat_intel.trending_score}")
    
    # OS Patches
    print("\nAvailable OS Patches:")
    for os_name, patch in vuln.os_patches.items():
        print(f"- {os_name}: {patch}")
    
    # Exploit References
    if vuln.references:
        print("\nExploit References:")
        for ref in vuln.references:
            print(f"- {ref}")
    
    # Risk Assessment
    print("\nRisk Assessment:")
    risk_factors = []
    
    if vuln.threat_intel.active_exploitation:
        risk_factors.append("Active exploitation in the wild")
    if vuln.threat_intel.threat_actors:
        risk_factors.append("Known threat actor involvement")
    if vuln.threat_intel.malware_families:
        risk_factors.append("Associated malware families")
    if vuln.emerging_threat:
        risk_factors.append("Emerging threat (high trending score)")
    
    print("Risk Factors:")
    for factor in risk_factors:
        print(f"- {factor}")

async def main():
    """Run the enhanced vulnerability analysis example"""
    await analyze_sbom_with_enhanced_feeds()

if __name__ == "__main__":
    asyncio.run(main())