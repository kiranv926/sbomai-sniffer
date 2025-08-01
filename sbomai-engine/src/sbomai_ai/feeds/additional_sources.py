"""
Additional specialized vulnerability data sources.
"""

import aiohttp
import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set
from abc import ABC, abstractmethod
import os
import re
from urllib.parse import quote_plus
import xml.etree.ElementTree as ET
import feedparser

from .vulnerability_sources import VulnerabilitySource

logger = logging.getLogger(__name__)

class MITRECVESource(VulnerabilitySource):
    """
    MITRE CVE Details integration
    Provides detailed CVE information and references
    """
    
    def __init__(self):
        self.base_url = "https://cve.mitre.org/cgi-bin/cvename.cgi"
    
    async def fetch_vulnerabilities(self, session: aiohttp.ClientSession, since: datetime) -> List[Dict]:
        # MITRE provides data through their CVE API
        params = {'name': f'CVE-{since.year}'}
        
        async with session.get(self.base_url, params=params) as response:
            if response.status == 200:
                data = await response.text()
                return self._parse_mitre_data(data)
        return []
    
    def _parse_mitre_data(self, data: str) -> List[Dict]:
        results = []
        # Parse HTML/XML response and extract CVE details
        # Implementation would parse MITRE's specific format
        return results

class CISAKEVSource(VulnerabilitySource):
    """
    CISA Known Exploited Vulnerabilities (KEV) Catalog
    Critical for identifying actively exploited vulnerabilities
    """
    
    def __init__(self):
        self.base_url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
    
    async def fetch_vulnerabilities(self, session: aiohttp.ClientSession, since: datetime) -> List[Dict]:
        async with session.get(self.base_url) as response:
            if response.status == 200:
                data = await response.json()
                return self._parse_cisa_data(data, since)
        return []
    
    def _parse_cisa_data(self, data: Dict, since: datetime) -> List[Dict]:
        results = []
        for vuln in data.get('vulnerabilities', []):
            date_added = datetime.strptime(vuln['dateAdded'], '%Y-%m-%d')
            if date_added >= since:
                results.append({
                    'source': 'cisa_kev',
                    'cve_id': vuln['cveID'],
                    'vendor': vuln['vendorProject'],
                    'product': vuln['product'],
                    'vulnerability_name': vuln['vulnerabilityName'],
                    'description': vuln['shortDescription'],
                    'required_action': vuln['requiredAction'],
                    'due_date': vuln['dueDate'],
                    'known_ransomware': vuln.get('knownRansomwareCampaignUse', False),
                    'notes': vuln.get('notes', '')
                })
        return results

class ExploitDBSource(VulnerabilitySource):
    """
    Offensive Security's Exploit Database
    Provides actual exploit code and proof of concepts
    """
    
    def __init__(self):
        self.base_url = "https://www.exploit-db.com/api/v1"
    
    async def fetch_vulnerabilities(self, session: aiohttp.ClientSession, since: datetime) -> List[Dict]:
        params = {'date_from': since.strftime('%Y-%m-%d')}
        
        async with session.get(f"{self.base_url}/exploits", params=params) as response:
            if response.status == 200:
                data = await response.json()
                return self._parse_exploitdb_data(data)
        return []
    
    def _parse_exploitdb_data(self, data: Dict) -> List[Dict]:
        results = []
        for exploit in data.get('data', []):
            results.append({
                'source': 'exploitdb',
                'edb_id': exploit['id'],
                'cve_id': exploit.get('cve', []),
                'title': exploit['title'],
                'description': exploit['description'],
                'type': exploit['type'],
                'platform': exploit['platform'],
                'author': exploit['author'],
                'published': exploit['date_published'],
                'verified': exploit['verified'],
                'exploit_url': f"https://www.exploit-db.com/exploits/{exploit['id']}"
            })
        return results

class RedHatSecuritySource(VulnerabilitySource):
    """
    Red Hat Security Data API
    Provides detailed security advisories and fixes
    """
    
    def __init__(self):
        self.base_url = "https://access.redhat.com/labs/securitydataapi/v1"
    
    async def fetch_vulnerabilities(self, session: aiohttp.ClientSession, since: datetime) -> List[Dict]:
        params = {'after': since.strftime('%Y-%m-%d')}
        
        async with session.get(f"{self.base_url}/cve.json", params=params) as response:
            if response.status == 200:
                data = await response.json()
                return self._parse_redhat_data(data)
        return []
    
    def _parse_redhat_data(self, data: List[Dict]) -> List[Dict]:
        results = []
        for vuln in data:
            results.append({
                'source': 'redhat',
                'cve_id': vuln['CVE'],
                'title': vuln.get('bugzilla', {}).get('description'),
                'public_date': vuln.get('public_date'),
                'severity': vuln.get('severity'),
                'cvss3_score': vuln.get('cvss3', {}).get('cvss3_base_score'),
                'cvss3_vector': vuln.get('cvss3', {}).get('cvss3_scoring_vector'),
                'affected_packages': vuln.get('affected_packages', []),
                'resource_url': vuln.get('resource_url'),
                'mitigation': vuln.get('mitigation'),
                'upstream_fix': vuln.get('upstream_fix')
            })
        return results

class AlpineSecDBSource(VulnerabilitySource):
    """
    Alpine Linux Security Database
    Tracks vulnerabilities in Alpine Linux packages
    """
    
    def __init__(self):
        self.base_url = "https://secdb.alpinelinux.org"
    
    async def fetch_vulnerabilities(self, session: aiohttp.ClientSession, since: datetime) -> List[Dict]:
        # Alpine provides security data by branch
        branches = ['v3.15', 'v3.16', 'v3.17', 'edge']
        results = []
        
        for branch in branches:
            url = f"{self.base_url}/{branch}/main.json"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    results.extend(self._parse_alpine_data(data, branch))
        
        return results
    
    def _parse_alpine_data(self, data: Dict, branch: str) -> List[Dict]:
        results = []
        for pkg_name, pkg_data in data.get('packages', {}).items():
            for version, vuln_data in pkg_data.get('versions', {}).items():
                for vuln in vuln_data.get('vulnerabilities', []):
                    results.append({
                        'source': 'alpine',
                        'branch': branch,
                        'package': pkg_name,
                        'version': version,
                        'cve_id': vuln.get('cve'),
                        'severity': vuln.get('severity'),
                        'fixed_version': vuln.get('fixed_version')
                    })
        return results

class JFrogXraySource(VulnerabilitySource):
    """
    JFrog Xray Security Data
    Provides vulnerability data with focus on artifacts and dependencies
    """
    
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
    
    async def fetch_vulnerabilities(self, session: aiohttp.ClientSession, since: datetime) -> List[Dict]:
        headers = {
            'X-JFrog-Art-Api': self.api_key,
            'Content-Type': 'application/json'
        }
        
        params = {
            'from_date': since.isoformat(),
            'order_by': 'created',
            'direction': 'asc'
        }
        
        async with session.get(
            f"{self.base_url}/api/v1/vulnerabilities",
            headers=headers,
            params=params
        ) as response:
            if response.status == 200:
                data = await response.json()
                return self._parse_xray_data(data)
        return []
    
    def _parse_xray_data(self, data: Dict) -> List[Dict]:
        results = []
        for vuln in data.get('vulnerabilities', []):
            results.append({
                'source': 'jfrog_xray',
                'cve_id': vuln.get('cve'),
                'provider': vuln.get('provider'),
                'summary': vuln.get('summary'),
                'severity': vuln.get('severity'),
                'cvss_v3_score': vuln.get('cvss_v3_score'),
                'impacted_artifacts': vuln.get('impacted_artifacts', []),
                'published': vuln.get('published'),
                'type': vuln.get('type'),
                'remediation': vuln.get('remediation')
            })
        return results

class UbuntuSecuritySource(VulnerabilitySource):
    """
    Ubuntu Security Tracker
    Provides Ubuntu-specific security updates and patches
    """
    
    def __init__(self):
        self.base_url = "https://ubuntu.com/security"
    
    async def fetch_vulnerabilities(self, session: aiohttp.ClientSession, since: datetime) -> List[Dict]:
        async with session.get(f"{self.base_url}/data/cve.json") as response:
            if response.status == 200:
                data = await response.json()
                return self._parse_ubuntu_data(data, since)
        return []
    
    def _parse_ubuntu_data(self, data: Dict, since: datetime) -> List[Dict]:
        results = []
        for cve_id, cve_data in data.items():
            if not isinstance(cve_data, dict):
                continue
                
            # Check if the CVE is recent enough
            published = cve_data.get('published')
            if published:
                pub_date = datetime.strptime(published, '%Y-%m-%d')
                if pub_date < since:
                    continue
            
            results.append({
                'source': 'ubuntu',
                'cve_id': cve_id,
                'description': cve_data.get('description'),
                'priority': cve_data.get('priority'),
                'status': cve_data.get('status'),
                'packages': cve_data.get('packages', {}),
                'published': published,
                'notes': cve_data.get('notes', [])
            })
        return results

class MetasploitSource(VulnerabilitySource):
    """
    Metasploit Framework Database
    Provides information about available exploit modules
    """
    
    def __init__(self):
        self.base_url = "https://raw.githubusercontent.com/rapid7/metasploit-framework/master"
    
    async def fetch_vulnerabilities(self, session: aiohttp.ClientSession, since: datetime) -> List[Dict]:
        # Fetch modules metadata
        async with session.get(f"{self.base_url}/db/modules_metadata_base.json") as response:
            if response.status == 200:
                data = await response.json()
                return self._parse_metasploit_data(data)
        return []
    
    def _parse_metasploit_data(self, data: List[Dict]) -> List[Dict]:
        results = []
        for module in data:
            if 'references' not in module:
                continue
            
            # Extract CVE references
            cve_refs = [
                ref for ref in module['references']
                if ref.startswith('CVE-')
            ]
            
            if cve_refs:
                results.append({
                    'source': 'metasploit',
                    'module_name': module['fullname'],
                    'module_type': module['type'],
                    'cve_ids': cve_refs,
                    'description': module.get('description'),
                    'rank': module.get('rank'),
                    'author': module.get('author', []),
                    'platform': module.get('platform', []),
                    'targets': module.get('targets', []),
                    'path': f"{self.base_url}/modules/{module['fullname']}"
                })
        return results

class VulnerabilitySourceManager:
    """
    Manages all vulnerability data sources and aggregates their data
    """
    
    def __init__(self, config: Dict):
        self.sources = {
            'mitre': MITRECVESource(),
            'cisa_kev': CISAKEVSource(),
            'exploitdb': ExploitDBSource(),
            'redhat': RedHatSecuritySource(),
            'alpine': AlpineSecDBSource(),
            'jfrog': JFrogXraySource(
                config.get('jfrog_api_key'),
                config.get('jfrog_base_url')
            ),
            'ubuntu': UbuntuSecuritySource(),
            'metasploit': MetasploitSource()
        }
    
    async def fetch_all(self, since: datetime) -> Dict[str, List[Dict]]:
        """Fetch vulnerabilities from all sources"""
        results = {}
        async with aiohttp.ClientSession() as session:
            tasks = []
            for source_name, source in self.sources.items():
                task = self._fetch_source(source_name, source, session, since)
                tasks.append(task)
            
            all_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for source_name, result in zip(self.sources.keys(), all_results):
                if isinstance(result, Exception):
                    logger.error(f"Error fetching from {source_name}: {result}")
                    results[source_name] = []
                else:
                    results[source_name] = result
        
        return results
    
    async def _fetch_source(self, source_name: str, source: VulnerabilitySource,
                          session: aiohttp.ClientSession, since: datetime) -> List[Dict]:
        """Fetch vulnerabilities from a specific source"""
        try:
            return await source.fetch_vulnerabilities(session, since)
        except Exception as e:
            logger.error(f"Error in {source_name}: {e}")
            raise

async def main():
    """Test the additional vulnerability sources"""
    config = {
        'jfrog_api_key': os.getenv('JFROG_API_KEY'),
        'jfrog_base_url': os.getenv('JFROG_URL')
    }
    
    manager = VulnerabilitySourceManager(config)
    since = datetime.now() - timedelta(days=7)
    
    results = await manager.fetch_all(since)
    
    # Print summary
    print("\nVulnerability Source Summary:")
    for source, vulns in results.items():
        print(f"{source}: {len(vulns)} vulnerabilities")

if __name__ == "__main__":
    asyncio.run(main())