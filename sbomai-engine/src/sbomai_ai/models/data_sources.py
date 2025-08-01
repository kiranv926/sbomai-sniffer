"""
Data source implementations for vulnerability intelligence
"""

import logging
from typing import Dict, List, Optional
import requests
import json
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

from ..utils.cache import Cache
from ..config import get_config

logger = logging.getLogger(__name__)

class BaseDataSource(ABC):
    """Base class for vulnerability data sources"""
    
    def __init__(self):
        self.config = get_config()
        self.cache = Cache()
        self.session = requests.Session()
    
    @abstractmethod
    def get_vulnerability(self, cve_id: str) -> Dict:
        """Get vulnerability data"""
        pass
    
    def _get_cached_or_fetch(self, key: str, fetch_func) -> Dict:
        """Get cached data or fetch from source"""
        cached = self.cache.get(key)
        if cached:
            return cached
        
        data = fetch_func()
        self.cache.set(key, data)
        return data

class NvdDataSource(BaseDataSource):
    """NVD API data source"""
    
    def __init__(self):
        super().__init__()
        # Handle missing config attributes gracefully
        try:
            self.api_key = getattr(self.config, 'nvd_api_key', None)
        except AttributeError:
            self.api_key = None
        self.base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        
        if self.api_key:
            self.session.headers.update({
                "apiKey": self.api_key
            })
    
    def get_vulnerability(self, cve_id: str) -> Dict:
        """Get vulnerability data from NVD"""
        def fetch():
            response = self.session.get(
                f"{self.base_url}/vulnerability/{cve_id}",
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            vuln = data['vulnerabilities'][0]['cve']
            metrics = vuln.get('metrics', {}).get('cvssMetricV31', [{}])[0]
            
            return {
                'description': vuln['descriptions'][0]['value'],
                'cvss_score': metrics.get('cvssData', {}).get('baseScore', 0.0),
                'cvss_vector': metrics.get('cvssData', {}).get('vectorString', ''),
                'cwe_id': vuln.get('weaknesses', [{}])[0].get('description', [{}])[0].get('value', ''),
                'published_date': vuln['published'],
                'last_modified_date': vuln['lastModified'],
                'references': [ref['url'] for ref in vuln.get('references', [])]
            }
        
        return self._get_cached_or_fetch(f"nvd_{cve_id}", fetch)

class OsvDataSource(BaseDataSource):
    """OSV API data source"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://api.osv.dev/v1"
    
    def get_vulnerability(self, cve_id: str) -> Dict:
        """Get vulnerability data from OSV"""
        def fetch():
            response = self.session.get(
                f"{self.base_url}/vulns/{cve_id}",
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                'affected_versions': self._extract_affected_versions(data),
                'fixed_versions': self._extract_fixed_versions(data),
                'ecosystem': data.get('affected', [{}])[0].get('package', {}).get('ecosystem', ''),
                'package_name': data.get('affected', [{}])[0].get('package', {}).get('name', '')
            }
        
        return self._get_cached_or_fetch(f"osv_{cve_id}", fetch)
    
    def _extract_affected_versions(self, data: Dict) -> List[str]:
        """Extract affected versions from OSV data"""
        versions = []
        for affected in data.get('affected', []):
            for version_range in affected.get('ranges', []):
                if version_range.get('type') == 'SEMVER':
                    versions.extend(version_range.get('events', []))
        return versions
    
    def _extract_fixed_versions(self, data: Dict) -> List[str]:
        """Extract fixed versions from OSV data"""
        versions = []
        for affected in data.get('affected', []):
            for version_range in affected.get('ranges', []):
                if version_range.get('type') == 'SEMVER':
                    for event in version_range.get('events', []):
                        if event.get('fixed', ''):
                            versions.append(event['fixed'])
        return versions

class GhsaDataSource(BaseDataSource):
    """GitHub Security Advisory API data source"""
    
    def __init__(self):
        super().__init__()
        self.token = self.config.data_sources.github_token
        self.base_url = "https://api.github.com/graphql"
        
        if self.token:
            self.session.headers.update({
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/vnd.github.v4+json"
            })
    
    def get_vulnerability(self, cve_id: str) -> Dict:
        """Get vulnerability data from GitHub Security Advisories"""
        advisory_data = self.get_advisory(cve_id)
        return {
            'source': 'ghsa',
            'cve_id': cve_id,
            'advisory_data': advisory_data,
            'affected_versions': advisory_data.get('vulnerable_version_range', ''),
            'fixed_versions': advisory_data.get('first_patched_version', ''),
            'repository_metadata': advisory_data.get('repository_metadata', {})
        }
    
    def get_advisory(self, cve_id: str) -> Dict:
        """Get advisory data from GitHub"""
        def fetch():
            # GraphQL query for advisory
            query = """
            query ($cveId: String!) {
              securityAdvisories(first: 1, orderBy: {field: UPDATED_AT, direction: DESC}, 
                               filterBy: {cveId: $cveId}) {
                nodes {
                  repository {
                    nameWithOwner
                    url
                    stargazerCount
                    forkCount
                  }
                  vulnerableVersionRange
                  firstPatchedVersion { identifier }
                  references
                }
              }
            }
            """
            
            response = self.session.post(
                self.base_url,
                json={'query': query, 'variables': {'cveId': cve_id}},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            advisory = data['data']['securityAdvisories']['nodes'][0]
            repo = advisory['repository']
            
            return {
                'repository_metadata': {
                    'name': repo['nameWithOwner'],
                    'url': repo['url'],
                    'stars': repo['stargazerCount'],
                    'forks': repo['forkCount']
                },
                'relevant_commits': self._get_relevant_commits(repo['nameWithOwner'], cve_id),
                'contributor_analysis': self._analyze_contributors(repo['nameWithOwner'])
            }
        
        return self._get_cached_or_fetch(f"ghsa_{cve_id}", fetch)
    
    def _get_relevant_commits(self, repo: str, cve_id: str) -> List[Dict]:
        """Get relevant commits for vulnerability"""
        # GraphQL query for commits
        query = """
        query ($repo: String!, $searchQuery: String!) {
          repository(owner: $repo.split('/')[0], name: $repo.split('/')[1]) {
            defaultBranchRef {
              target {
                ... on Commit {
                  history(first: 10, query: $searchQuery) {
                    nodes {
                      oid
                      messageHeadline
                      committedDate
                      author { name email }
                    }
                  }
                }
              }
            }
          }
        }
        """
        
        search_query = f"security fix CVE-{cve_id}"
        
        response = self.session.post(
            self.base_url,
            json={'query': query, 'variables': {
                'repo': repo,
                'searchQuery': search_query
            }},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        return data['data']['repository']['defaultBranchRef']['target']['history']['nodes']
    
    def _analyze_contributors(self, repo: str) -> Dict:
        """Analyze repository contributors"""
        # GraphQL query for contributors
        query = """
        query ($repo: String!) {
          repository(owner: $repo.split('/')[0], name: $repo.split('/')[1]) {
            collaborators(first: 100) {
              nodes {
                login
                contributionsCollection {
                  totalCommitContributions
                  totalIssueContributions
                  totalPullRequestContributions
                  totalPullRequestReviewContributions
                }
              }
            }
          }
        }
        """
        
        response = self.session.post(
            self.base_url,
            json={'query': query, 'variables': {'repo': repo}},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        contributors = data['data']['repository']['collaborators']['nodes']
        
        return {
            'total_contributors': len(contributors),
            'contribution_stats': self._calculate_contribution_stats(contributors),
            'top_contributors': self._get_top_contributors(contributors)
        }
    
    def _calculate_contribution_stats(self, contributors: List[Dict]) -> Dict:
        """Calculate contributor statistics"""
        total_commits = sum(c['contributionsCollection']['totalCommitContributions'] for c in contributors)
        total_prs = sum(c['contributionsCollection']['totalPullRequestContributions'] for c in contributors)
        total_reviews = sum(c['contributionsCollection']['totalPullRequestReviewContributions'] for c in contributors)
        
        return {
            'avg_commits_per_contributor': total_commits / len(contributors),
            'avg_prs_per_contributor': total_prs / len(contributors),
            'avg_reviews_per_contributor': total_reviews / len(contributors)
        }
    
    def _get_top_contributors(self, contributors: List[Dict], limit: int = 5) -> List[Dict]:
        """Get top contributors by total contributions"""
        sorted_contributors = sorted(
            contributors,
            key=lambda c: sum(c['contributionsCollection'].values()),
            reverse=True
        )
        
        return [{
            'login': c['login'],
            'total_contributions': sum(c['contributionsCollection'].values())
        } for c in sorted_contributors[:limit]]

class ExploitDbDataSource(BaseDataSource):
    """Exploit-DB data source"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.exploit-db.com/api/v1"
    
    def get_exploits(self, cve_id: str) -> List[Dict]:
        """Get exploits from Exploit-DB"""
        def fetch():
            response = self.session.get(
                f"{self.base_url}/search",
                params={'cve': cve_id},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            return [{
                'id': exploit['id'],
                'title': exploit['title'],
                'type': exploit['type'],
                'platform': exploit['platform'],
                'author': exploit['author'],
                'published': exploit['date_published'],
                'verified': exploit['verified'],
                'url': f"https://www.exploit-db.com/exploits/{exploit['id']}"
            } for exploit in data['data']]
        
        return self._get_cached_or_fetch(f"exploitdb_{cve_id}", fetch)

class MitreDataSource(BaseDataSource):
    """MITRE ATT&CK data source"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://cti-taxii.mitre.org/stix/attack/v9.0"
    
    def get_attack_patterns(self, cve_id: str) -> List[str]:
        """Get related ATT&CK patterns"""
        def fetch():
            # This is a simplified example - real implementation would use STIX/TAXII
            # to fetch ATT&CK data
            return [
                "T1190: Exploit Public-Facing Application",
                "T1203: Exploitation for Client Execution",
                "T1211: Exploitation for Defense Evasion"
            ]
        
        return self._get_cached_or_fetch(f"mitre_{cve_id}", fetch)

class CisaKevDataSource(BaseDataSource):
    """CISA Known Exploited Vulnerabilities (KEV) data source"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
    
    def is_known_exploited(self, cve_id: str) -> bool:
        """Check if vulnerability is in KEV catalog"""
        def fetch():
            response = self.session.get(self.base_url, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            return any(vuln['cveID'] == cve_id for vuln in data['vulnerabilities'])
        
        return self._get_cached_or_fetch(f"kev_{cve_id}", fetch)

class RedHatDataSource(BaseDataSource):
    """Red Hat Security Data API source"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://access.redhat.com/labs/securitydataapi/v1"
    
    def get_analysis(self, cve_id: str) -> Dict:
        """Get Red Hat's vulnerability analysis"""
        def fetch():
            response = self.session.get(
                f"{self.base_url}/cve/{cve_id}.json",
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                'statement': data.get('statement', ''),
                'mitigation': data.get('mitigation', ''),
                'severity': data.get('severity', ''),
                'impact': data.get('impact', ''),
                'package_state': data.get('package_state', [])
            }
        
        return self._get_cached_or_fetch(f"redhat_{cve_id}", fetch)

class JFrogDataSource(BaseDataSource):
    """JFrog Security Research data source"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://security-research.jfrog.com/api/v1"
        self.api_key = self.config.data_sources.jfrog_api_key
        
        if self.api_key:
            self.session.headers.update({
                "X-JFrog-API-Key": self.api_key
            })
    
    def get_research(self, cve_id: str) -> Dict:
        """Get JFrog's security research data"""
        def fetch():
            response = self.session.get(
                f"{self.base_url}/vulnerabilities/{cve_id}",
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                'research_summary': data.get('research_summary', ''),
                'root_cause': data.get('root_cause', ''),
                'exploit_status': data.get('exploit_status', ''),
                'research_score': data.get('research_score', 0.0),
                'malware_status': data.get('malware_status', False)
            }
        
        return self._get_cached_or_fetch(f"jfrog_{cve_id}", fetch) 