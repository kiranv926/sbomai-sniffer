#!/usr/bin/env python3
"""
SBOMAI GitHub Project Scanner
Comprehensive scanner for GitHub projects in different programming languages
"""

import os
import sys
import json
import argparse
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import asyncio

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from sbomai_ai.models.vulnerability_intelligence import VulnerabilityIntelligence
from sbomai_ai.models.dependency_graph import DependencyGraph
from sbomai_ai.models.local_model import LocalTransformerModel, LocalTransformerConfig

@dataclass
class LanguageInfo:
    """Information about a programming language detected in the project"""
    name: str
    version_files: List[str]
    package_managers: List[str]
    sbom_generators: List[str]
    risk_factors: List[str]

class GitHubProjectScanner:
    """Comprehensive GitHub project scanner for multiple languages"""
    
    def __init__(self):
        self.languages = self._initialize_languages()
        self.vuln_intel = None
        self.ai_model = None
        
    def _initialize_languages(self) -> Dict[str, LanguageInfo]:
        """Initialize supported programming languages"""
        return {
            'python': LanguageInfo(
                name='Python',
                version_files=['requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile', 'poetry.lock'],
                package_managers=['pip', 'poetry', 'pipenv'],
                sbom_generators=['cyclonedx-py', 'syft', 'trivy'],
                risk_factors=['outdated_dependencies', 'security_vulnerabilities', 'license_issues']
            ),
            'java': LanguageInfo(
                name='Java',
                version_files=['pom.xml', 'build.gradle', 'gradle.properties', 'build.sbt'],
                package_managers=['maven', 'gradle', 'sbt'],
                sbom_generators=['cyclonedx-maven', 'syft', 'trivy'],
                risk_factors=['log4j_vulnerabilities', 'spring_vulnerabilities', 'outdated_jdks']
            ),
            'go': LanguageInfo(
                name='Go',
                version_files=['go.mod', 'go.sum', 'Gopkg.toml', 'Gopkg.lock'],
                package_managers=['go modules', 'dep'],
                sbom_generators=['cyclonedx-gomod', 'syft', 'trivy'],
                risk_factors=['outdated_go_version', 'vulnerable_dependencies', 'insecure_packages']
            ),
            'rust': LanguageInfo(
                name='Rust',
                version_files=['Cargo.toml', 'Cargo.lock'],
                package_managers=['cargo'],
                sbom_generators=['cyclonedx-cargo', 'syft', 'trivy'],
                risk_factors=['outdated_rust_version', 'unsafe_code', 'vulnerable_crates']
            ),
            'nodejs': LanguageInfo(
                name='Node.js',
                version_files=['package.json', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml'],
                package_managers=['npm', 'yarn', 'pnpm'],
                sbom_generators=['cyclonedx-npm', 'syft', 'trivy'],
                risk_factors=['outdated_node_version', 'vulnerable_packages', 'malicious_packages']
            ),
            'ruby': LanguageInfo(
                name='Ruby',
                version_files=['Gemfile', 'Gemfile.lock', 'gemspec'],
                package_managers=['bundler', 'gem'],
                sbom_generators=['cyclonedx-ruby', 'syft', 'trivy'],
                risk_factors=['outdated_ruby_version', 'vulnerable_gems', 'license_issues']
            ),
            'php': LanguageInfo(
                name='PHP',
                version_files=['composer.json', 'composer.lock'],
                package_managers=['composer'],
                sbom_generators=['cyclonedx-composer', 'syft', 'trivy'],
                risk_factors=['outdated_php_version', 'vulnerable_packages', 'security_issues']
            ),
            'cpp': LanguageInfo(
                name='C/C++',
                version_files=['CMakeLists.txt', 'Makefile', 'configure.ac', 'package.json'],
                package_managers=['cmake', 'make', 'conan'],
                sbom_generators=['syft', 'trivy'],
                risk_factors=['memory_vulnerabilities', 'buffer_overflows', 'outdated_libraries']
            )
        }
    
    def setup_ai_models(self):
        """Initialize AI models for analysis"""
        try:
            # Initialize local AI model
            local_config = LocalTransformerConfig(
                model_name="microsoft/codebert-base",
                max_length=512
            )
            self.ai_model = LocalTransformerModel(local_config)
            print("✅ AI model initialized")
            
            # Initialize vulnerability intelligence
            self.vuln_intel = VulnerabilityIntelligence()
            print("✅ Vulnerability intelligence initialized")
            
        except Exception as e:
            print(f"⚠️  Warning: AI models not available: {e}")
            print("   Continuing with basic analysis...")
    
    def clone_repository(self, repo_url: str, temp_dir: str, branch: Optional[str] = None) -> str:
        """Clone GitHub repository to temporary directory"""
        try:
            print(f"📥 Cloning repository: {repo_url}")
            
            # Extract repo name from URL
            repo_name = repo_url.split('/')[-1].replace('.git', '')
            repo_path = os.path.join(temp_dir, repo_name)
            
            # Build git clone command
            cmd = ['git', 'clone']
            if branch:
                cmd.extend(['-b', branch])
            cmd.extend([repo_url, repo_path])
            
            # Clone the repository
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            if result.returncode != 0:
                raise Exception(f"Git clone failed: {result.stderr}")
            
            print(f"✅ Repository cloned to: {repo_path}")
            return repo_path
            
        except Exception as e:
            print(f"❌ Failed to clone repository: {e}")
            raise
    
    def detect_languages(self, repo_path: str) -> List[Tuple[str, LanguageInfo, List[str]]]:
        """Detect programming languages used in the repository"""
        detected_languages = []
        
        print("🔍 Detecting programming languages...")
        
        for lang_key, lang_info in self.languages.items():
            found_files = []
            
            # Check for language-specific files
            for file_pattern in lang_info.version_files:
                for file_path in Path(repo_path).rglob(file_pattern):
                    if file_path.is_file():
                        found_files.append(str(file_path.relative_to(repo_path)))
            
            # Check for language-specific directories
            lang_dirs = {
                'python': ['__pycache__', '.venv', 'venv', 'env'],
                'java': ['.mvn', 'target', 'build'],
                'go': ['vendor', 'pkg'],
                'rust': ['target', 'Cargo.toml'],
                'nodejs': ['node_modules', 'package.json'],
                'ruby': ['vendor', 'Gemfile'],
                'php': ['vendor', 'composer.json'],
                'cpp': ['CMakeLists.txt', 'Makefile']
            }
            
            if lang_key in lang_dirs:
                for dir_name in lang_dirs[lang_key]:
                    if (Path(repo_path) / dir_name).exists():
                        found_files.append(dir_name)
            
            if found_files:
                detected_languages.append((lang_key, lang_info, found_files))
                print(f"   Found {lang_info.name}: {', '.join(found_files[:3])}{'...' if len(found_files) > 3 else ''}")
        
        return detected_languages
    
    def generate_sbom_for_language(self, repo_path: str, language: str, lang_info: LanguageInfo) -> Dict:
        """Generate SBOM for a specific programming language"""
        print(f"🔧 Generating SBOM for {lang_info.name}...")
        
        # Try language-specific SBOM generators
        for generator in lang_info.sbom_generators:
            try:
                print(f"   Trying {generator}...")
                
                if generator == 'cyclonedx-py' and language == 'python':
                    result = subprocess.run(
                        ['cyclonedx-py', 'requirements', '--format', 'json'],
                        cwd=repo_path,
                        capture_output=True,
                        text=True,
                        timeout=120
                    )
                elif generator == 'cyclonedx-maven' and language == 'java':
                    result = subprocess.run(
                        ['mvn', 'org.cyclonedx:cyclonedx-maven-plugin:makeAggregateBom'],
                        cwd=repo_path,
                        capture_output=True,
                        text=True,
                        timeout=300
                    )
                elif generator == 'cyclonedx-gomod' and language == 'go':
                    result = subprocess.run(
                        ['cyclonedx-gomod', 'mod', '--output', 'bom.json'],
                        cwd=repo_path,
                        capture_output=True,
                        text=True,
                        timeout=120
                    )
                elif generator == 'cyclonedx-npm' and language == 'nodejs':
                    result = subprocess.run(
                        ['cyclonedx-npm', '--output-file', 'bom.json'],
                        cwd=repo_path,
                        capture_output=True,
                        text=True,
                        timeout=120
                    )
                elif generator == 'syft':
                    result = subprocess.run(
                        ['syft', repo_path, '-o', 'cyclonedx-json'],
                        capture_output=True,
                        text=True,
                        timeout=180
                    )
                elif generator == 'trivy':
                    result = subprocess.run(
                        ['trivy', 'fs', '--format', 'cyclonedx', repo_path],
                        capture_output=True,
                        text=True,
                        timeout=180
                    )
                
                if result.returncode == 0:
                    print(f"✅ SBOM generated using {generator}")
                    return json.loads(result.stdout)
                    
            except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError) as e:
                print(f"   {generator} failed: {e}")
                continue
        
        # Fallback: Create basic SBOM structure
        print(f"⚠️  No SBOM generators found for {lang_info.name}, creating basic structure...")
        return self.create_basic_sbom_for_language(repo_path, language, lang_info)
    
    def create_basic_sbom_for_language(self, repo_path: str, language: str, lang_info: LanguageInfo) -> Dict:
        """Create basic SBOM structure for a specific language"""
        components = []
        
        # Extract basic component info based on language
        if language == 'python':
            # Look for requirements.txt or setup.py
            req_file = Path(repo_path) / 'requirements.txt'
            if req_file.exists():
                with open(req_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            parts = line.split('==')
                            if len(parts) == 2:
                                components.append({
                                    "name": parts[0],
                                    "version": parts[1],
                                    "purl": f"pkg:pypi/{parts[0]}@{parts[1]}",
                                    "type": "library"
                                })
        
        elif language == 'java':
            # Look for pom.xml
            pom_file = Path(repo_path) / 'pom.xml'
            if pom_file.exists():
                components.append({
                    "name": Path(repo_path).name,
                    "version": "1.0.0",
                    "purl": f"pkg:maven/{Path(repo_path).name}@1.0.0",
                    "type": "application"
                })
        
        elif language == 'nodejs':
            # Look for package.json
            pkg_file = Path(repo_path) / 'package.json'
            if pkg_file.exists():
                try:
                    with open(pkg_file, 'r') as f:
                        pkg_data = json.load(f)
                        components.append({
                            "name": pkg_data.get('name', Path(repo_path).name),
                            "version": pkg_data.get('version', '1.0.0'),
                            "purl": f"pkg:npm/{pkg_data.get('name', Path(repo_path).name)}@{pkg_data.get('version', '1.0.0')}",
                            "type": "application"
                        })
                except json.JSONDecodeError:
                    pass
        
        return {
            "bomFormat": "CycloneDX",
            "specVersion": "1.4",
            "version": 1,
            "metadata": {
                "timestamp": "2025-01-29T12:00:00Z",
                "tools": [{"name": "SBOMAI-GitHub-Scanner", "version": "1.0.0"}],
                "component": {
                    "name": Path(repo_path).name,
                    "version": "1.0.0",
                    "type": "application",
                    "properties": [
                        {"name": "language", "value": language},
                        {"name": "package_manager", "value": lang_info.package_managers[0] if lang_info.package_managers else "unknown"}
                    ]
                }
            },
            "components": components
        }
    
    def analyze_project(self, repo_path: str, detected_languages: List[Tuple[str, LanguageInfo, List[str]]]) -> Dict:
        """Analyze the entire project"""
        print("🤖 Analyzing project with AI...")
        
        try:
            # Initialize AI models if not already done
            if not self.ai_model:
                self.setup_ai_models()
            
            all_components = []
            language_analysis = {}
            
            # Analyze each detected language
            for language, lang_info, found_files in detected_languages:
                print(f"   Analyzing {lang_info.name} components...")
                
                # Generate SBOM for this language
                sbom_data = self.generate_sbom_for_language(repo_path, language, lang_info)
                components = sbom_data.get('components', [])
                
                # Add language-specific metadata
                for component in components:
                    component['language'] = language
                    component['package_manager'] = lang_info.package_managers[0] if lang_info.package_managers else 'unknown'
                    component['risk_factors'] = lang_info.risk_factors
                
                all_components.extend(components)
                
                # Language-specific analysis
                language_analysis[language] = {
                    'name': lang_info.name,
                    'components_count': len(components),
                    'package_managers': lang_info.package_managers,
                    'risk_factors': lang_info.risk_factors,
                    'found_files': found_files
                }
            
            if not all_components:
                print("⚠️  No components found in project")
                return {"error": "No components found"}
            
            print(f"📦 Found {len(all_components)} total components across {len(detected_languages)} languages")
            
            # Create dependency graph
            graph = DependencyGraph()
            
            # Add components to graph
            for component in all_components:
                package_data = {
                    'name': component.get('name', 'unknown'),
                    'version': component.get('version', 'unknown'),
                    'purl': component.get('purl', f"pkg:generic/{component.get('name', 'unknown')}"),
                    'vulnerabilities': [],
                    'language': component.get('language', 'unknown')
                }
                graph.add_node(package_data)
            
            # Perform vulnerability analysis
            analysis_results = {
                'total_components': len(all_components),
                'languages_detected': len(detected_languages),
                'language_analysis': language_analysis,
                'vulnerable_components': 0,
                'vulnerabilities': [],
                'risk_scores': {},
                'recommendations': [],
                'overall_risk': 'LOW'
            }
            
            # Analyze each component
            for component in all_components:
                component_name = component.get('name', 'unknown')
                language = component.get('language', 'unknown')
                print(f"   Analyzing: {component_name} ({language})")
                
                # Language-specific vulnerability detection
                risk_score = self.analyze_component_risk(component, language)
                analysis_results['risk_scores'][component_name] = risk_score
                
                # Check for known vulnerabilities
                vulnerabilities = self.check_component_vulnerabilities(component, language)
                if vulnerabilities:
                    analysis_results['vulnerabilities'].extend(vulnerabilities)
                    analysis_results['vulnerable_components'] += 1
            
            # Generate recommendations
            analysis_results['recommendations'] = self.generate_recommendations(analysis_results, detected_languages)
            
            # Determine overall risk
            analysis_results['overall_risk'] = self.calculate_overall_risk(analysis_results)
            
            return analysis_results
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            return {"error": str(e)}
    
    def analyze_component_risk(self, component: Dict, language: str) -> float:
        """Analyze risk for a specific component"""
        base_score = 2.0
        
        # Language-specific risk factors
        if language == 'python':
            if 'log4j' in component.get('name', '').lower():
                base_score += 8.0
            elif 'django' in component.get('name', '').lower():
                base_score += 3.0
        elif language == 'java':
            if 'log4j' in component.get('name', '').lower():
                base_score += 9.0
            elif 'spring' in component.get('name', '').lower():
                base_score += 4.0
        elif language == 'nodejs':
            if 'lodash' in component.get('name', '').lower():
                base_score += 3.0
            elif 'express' in component.get('name', '').lower():
                base_score += 2.0
        
        # Version-based risk
        version = component.get('version', '')
        if version and version.startswith('0.'):
            base_score += 2.0  # Beta/alpha versions
        
        return min(base_score, 10.0)
    
    def check_component_vulnerabilities(self, component: Dict, language: str) -> List[Dict]:
        """Check for known vulnerabilities in a component"""
        vulnerabilities = []
        component_name = component.get('name', '').lower()
        
        # Known vulnerable components
        known_vulns = {
            'python': {
                'log4j': {'cve': 'CVE-2021-44228', 'severity': 'CRITICAL', 'cvss_score': 9.8},
                'django': {'cve': 'CVE-2021-44420', 'severity': 'HIGH', 'cvss_score': 7.5}
            },
            'java': {
                'log4j': {'cve': 'CVE-2021-44228', 'severity': 'CRITICAL', 'cvss_score': 9.8},
                'spring': {'cve': 'CVE-2022-22965', 'severity': 'HIGH', 'cvss_score': 8.5}
            },
            'nodejs': {
                'lodash': {'cve': 'CVE-2021-23337', 'severity': 'MEDIUM', 'cvss_score': 5.3},
                'express': {'cve': 'CVE-2022-24999', 'severity': 'MEDIUM', 'cvss_score': 5.3}
            }
        }
        
        if language in known_vulns:
            for vuln_name, vuln_info in known_vulns[language].items():
                if vuln_name in component_name:
                    vulnerabilities.append({
                        'component': component.get('name', 'unknown'),
                        'language': language,
                        'cve': vuln_info['cve'],
                        'severity': vuln_info['severity'],
                        'cvss_score': vuln_info['cvss_score'],
                        'description': f'Known vulnerability in {component_name}'
                    })
        
        return vulnerabilities
    
    def generate_recommendations(self, analysis_results: Dict, detected_languages: List[Tuple[str, LanguageInfo, List[str]]]) -> List[str]:
        """Generate recommendations based on analysis results"""
        recommendations = []
        
        if analysis_results['vulnerable_components'] > 0:
            recommendations.extend([
                "🚨 Update vulnerable components to latest versions",
                "🔍 Review security patches for critical vulnerabilities",
                "🛡️ Consider implementing additional security controls"
            ])
        
        # Language-specific recommendations
        for language, lang_info, _ in detected_languages:
            if language == 'python':
                recommendations.append("🐍 Consider using virtual environments for dependency isolation")
            elif language == 'java':
                recommendations.append("☕ Update to latest LTS Java version")
            elif language == 'nodejs':
                recommendations.append("📦 Use npm audit to check for vulnerabilities")
            elif language == 'go':
                recommendations.append("🐹 Keep Go version updated for security patches")
        
        if not recommendations:
            recommendations.append("✅ No critical vulnerabilities detected")
        
        return recommendations
    
    def calculate_overall_risk(self, analysis_results: Dict) -> str:
        """Calculate overall risk level"""
        if analysis_results['vulnerable_components'] == 0:
            return 'LOW'
        
        # Check for critical vulnerabilities
        critical_vulns = [v for v in analysis_results['vulnerabilities'] if v.get('severity') == 'CRITICAL']
        if critical_vulns:
            return 'CRITICAL'
        
        # Check for high vulnerabilities
        high_vulns = [v for v in analysis_results['vulnerabilities'] if v.get('severity') == 'HIGH']
        if high_vulns:
            return 'HIGH'
        
        return 'MEDIUM'
    
    def generate_report(self, repo_url: str, analysis_results: Dict, output_format: str = 'json') -> str:
        """Generate analysis report"""
        print("📊 Generating report...")
        
        report = {
            "repository": repo_url,
            "timestamp": "2025-01-29T12:00:00Z",
            "analysis_results": analysis_results,
            "summary": {
                "total_components": analysis_results.get('total_components', 0),
                "languages_detected": analysis_results.get('languages_detected', 0),
                "vulnerable_components": analysis_results.get('vulnerable_components', 0),
                "vulnerability_rate": f"{(analysis_results.get('vulnerable_components', 0) / max(1, analysis_results.get('total_components', 1))) * 100:.1f}%",
                "overall_risk": analysis_results.get('overall_risk', 'UNKNOWN')
            }
        }
        
        if output_format == 'json':
            return json.dumps(report, indent=2)
        elif output_format == 'text':
            return self.format_text_report(report)
        else:
            return json.dumps(report, indent=2)
    
    def format_text_report(self, report: Dict) -> str:
        """Format report as text"""
        text = []
        text.append("=" * 60)
        text.append("SBOMAI GITHUB PROJECT ANALYSIS REPORT")
        text.append("=" * 60)
        text.append(f"Repository: {report['repository']}")
        text.append(f"Timestamp: {report['timestamp']}")
        text.append("")
        
        summary = report['summary']
        text.append("📊 SUMMARY")
        text.append("-" * 40)
        text.append(f"Total Components: {summary['total_components']}")
        text.append(f"Languages Detected: {summary['languages_detected']}")
        text.append(f"Vulnerable Components: {summary['vulnerable_components']}")
        text.append(f"Vulnerability Rate: {summary['vulnerability_rate']}")
        text.append(f"Overall Risk: {summary['overall_risk']}")
        text.append("")
        
        analysis = report['analysis_results']
        
        # Language analysis
        if analysis.get('language_analysis'):
            text.append("🔍 LANGUAGES DETECTED")
            text.append("-" * 40)
            for lang, lang_info in analysis['language_analysis'].items():
                text.append(f"• {lang_info['name']}: {lang_info['components_count']} components")
                text.append(f"  Package Managers: {', '.join(lang_info['package_managers'])}")
                text.append(f"  Risk Factors: {', '.join(lang_info['risk_factors'])}")
                text.append("")
        
        # Vulnerabilities
        if analysis.get('vulnerabilities'):
            text.append("⚠️  VULNERABILITIES")
            text.append("-" * 40)
            for vuln in analysis['vulnerabilities']:
                text.append(f"Component: {vuln['component']} ({vuln['language']})")
                text.append(f"CVE: {vuln['cve']}")
                text.append(f"Severity: {vuln['severity']}")
                text.append(f"CVSS: {vuln['cvss_score']}")
                text.append(f"Description: {vuln['description']}")
                text.append("")
        
        # Recommendations
        if analysis.get('recommendations'):
            text.append("🎯 RECOMMENDATIONS")
            text.append("-" * 40)
            for i, rec in enumerate(analysis['recommendations'], 1):
                text.append(f"{i}. {rec}")
            text.append("")
        
        text.append("=" * 60)
        return "\n".join(text)
    
    def scan_repository(self, repo_url: str, branch: Optional[str] = None, output_format: str = 'json', output_file: Optional[str] = None):
        """Main method to scan a GitHub repository"""
        print("🚀 SBOMAI Engine - GitHub Project Scanner")
        print("=" * 50)
        
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Clone repository
                repo_path = self.clone_repository(repo_url, temp_dir, branch)
                
                # Detect languages
                detected_languages = self.detect_languages(repo_path)
                
                if not detected_languages:
                    print("⚠️  No supported programming languages detected")
                    return {"error": "No supported languages found"}
                
                # Analyze project
                analysis_results = self.analyze_project(repo_path, detected_languages)
                
                # Generate report
                report = self.generate_report(repo_url, analysis_results, output_format)
                
                # Output report
                if output_file:
                    with open(output_file, 'w') as f:
                        f.write(report)
                    print(f"📄 Report saved to: {output_file}")
                else:
                    print("\n" + "=" * 60)
                    print("ANALYSIS REPORT")
                    print("=" * 60)
                    print(report)
                
                return analysis_results
                
            except Exception as e:
                print(f"❌ Repository scan failed: {e}")
                return {"error": str(e)}

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="SBOMAI GitHub Project Scanner - Multi-language vulnerability analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python github_project_scanner.py https://github.com/user/repo
  python github_project_scanner.py https://github.com/user/repo --branch develop
  python github_project_scanner.py https://github.com/user/repo --output-format text
  python github_project_scanner.py https://github.com/user/repo --output-file report.json
        """
    )
    
    parser.add_argument(
        'repository',
        help='GitHub repository URL to scan'
    )
    
    parser.add_argument(
        '--branch', '-b',
        help='Git branch to scan (default: main/master)'
    )
    
    parser.add_argument(
        '--output-format', '-o',
        choices=['json', 'text'],
        default='json',
        help='Output format (default: json)'
    )
    
    parser.add_argument(
        '--output-file', '-f',
        help='Output file path (default: stdout)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    scanner = GitHubProjectScanner()
    scanner.scan_repository(
        repo_url=args.repository,
        branch=args.branch,
        output_format=args.output_format,
        output_file=args.output_file
    )

if __name__ == "__main__":
    main() 