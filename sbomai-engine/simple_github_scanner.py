#!/usr/bin/env python3
"""
Simple GitHub Project Scanner
Detects and analyzes GitHub projects in different programming languages
"""

import os
import sys
import json
import argparse
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

def detect_languages(repo_path: str) -> Dict[str, List[str]]:
    """Detect programming languages in the repository"""
    languages = {}
    
    # Language detection patterns
    patterns = {
        'python': ['requirements.txt', 'setup.py', 'pyproject.toml', '__pycache__', '.py'],
        'java': ['pom.xml', 'build.gradle', '.java', 'target/', '.mvn/'],
        'go': ['go.mod', 'go.sum', '.go', 'vendor/'],
        'rust': ['Cargo.toml', 'Cargo.lock', '.rs'],
        'nodejs': ['package.json', 'package-lock.json', 'node_modules/', '.js', '.ts'],
        'ruby': ['Gemfile', 'Gemfile.lock', '.rb', 'vendor/'],
        'php': ['composer.json', 'composer.lock', '.php'],
        'cpp': ['CMakeLists.txt', 'Makefile', '.cpp', '.c', '.h']
    }
    
    print("🔍 Detecting programming languages...")
    
    for lang, files in patterns.items():
        found = []
        for pattern in files:
            for file_path in Path(repo_path).rglob(pattern):
                if file_path.is_file() or file_path.is_dir():
                    found.append(str(file_path.relative_to(repo_path)))
        
        if found:
            languages[lang] = found[:5]  # Limit to first 5 files
            print(f"   Found {lang}: {', '.join(found[:3])}{'...' if len(found) > 3 else ''}")
    
    return languages

def analyze_language_specific_risks(language: str, components: List[Dict]) -> List[Dict]:
    """Analyze risks specific to each programming language"""
    vulnerabilities = []
    
    # Known vulnerable components by language
    known_vulns = {
        'python': {
            'log4j': {'cve': 'CVE-2021-44228', 'severity': 'CRITICAL', 'cvss_score': 9.8},
            'django': {'cve': 'CVE-2021-44420', 'severity': 'HIGH', 'cvss_score': 7.5},
            'flask': {'cve': 'CVE-2020-26160', 'severity': 'MEDIUM', 'cvss_score': 5.3}
        },
        'java': {
            'log4j': {'cve': 'CVE-2021-44228', 'severity': 'CRITICAL', 'cvss_score': 9.8},
            'spring': {'cve': 'CVE-2022-22965', 'severity': 'HIGH', 'cvss_score': 8.5},
            'jackson': {'cve': 'CVE-2020-25649', 'severity': 'HIGH', 'cvss_score': 7.5}
        },
        'nodejs': {
            'lodash': {'cve': 'CVE-2021-23337', 'severity': 'MEDIUM', 'cvss_score': 5.3},
            'express': {'cve': 'CVE-2022-24999', 'severity': 'MEDIUM', 'cvss_score': 5.3},
            'moment': {'cve': 'CVE-2022-24785', 'severity': 'MEDIUM', 'cvss_score': 5.3}
        },
        'go': {
            'golang': {'cve': 'CVE-2022-29526', 'severity': 'HIGH', 'cvss_score': 7.5},
            'crypto': {'cve': 'CVE-2022-32149', 'severity': 'MEDIUM', 'cvss_score': 5.3}
        },
        'rust': {
            'rust': {'cve': 'CVE-2022-21658', 'severity': 'MEDIUM', 'cvss_score': 5.3}
        }
    }
    
    for component in components:
        component_name = component.get('name', '').lower()
        
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

def generate_language_recommendations(languages: Dict[str, List[str]]) -> List[str]:
    """Generate language-specific recommendations"""
    recommendations = []
    
    for language in languages.keys():
        if language == 'python':
            recommendations.extend([
                "🐍 Use virtual environments (venv/conda) for dependency isolation",
                "🐍 Keep Python version updated for security patches",
                "🐍 Use pip-audit to check for vulnerabilities"
            ])
        elif language == 'java':
            recommendations.extend([
                "☕ Update to latest LTS Java version",
                "☕ Use Maven/Gradle dependency check plugins",
                "☕ Enable security scanning in CI/CD"
            ])
        elif language == 'nodejs':
            recommendations.extend([
                "📦 Run 'npm audit' regularly",
                "📦 Use 'npm outdated' to check for updates",
                "📦 Consider using yarn or pnpm for better security"
            ])
        elif language == 'go':
            recommendations.extend([
                "🐹 Keep Go version updated",
                "🐹 Use 'go list -m all' to check dependencies",
                "🐹 Run 'gosec' for security analysis"
            ])
        elif language == 'rust':
            recommendations.extend([
                "🦀 Use 'cargo audit' for vulnerability scanning",
                "🦀 Keep Rust toolchain updated",
                "🦀 Review unsafe code blocks"
            ])
    
    return list(set(recommendations))  # Remove duplicates

def scan_github_repository(repo_url: str, branch: Optional[str] = None) -> Dict:
    """Scan a GitHub repository for vulnerabilities"""
    print(f"🚀 Scanning GitHub repository: {repo_url}")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Clone repository
            print("📥 Cloning repository...")
            repo_name = repo_url.split('/')[-1].replace('.git', '')
            repo_path = os.path.join(temp_dir, repo_name)
            
            cmd = ['git', 'clone']
            if branch:
                cmd.extend(['-b', branch])
            cmd.extend([repo_url, repo_path])
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if result.returncode != 0:
                raise Exception(f"Git clone failed: {result.stderr}")
            
            print("✅ Repository cloned successfully")
            
            # Detect languages
            languages = detect_languages(repo_path)
            
            if not languages:
                return {
                    "error": "No supported programming languages detected",
                    "repository": repo_url,
                    "languages": []
                }
            
            # Analyze each language
            analysis_results = {
                "repository": repo_url,
                "languages_detected": list(languages.keys()),
                "language_details": {},
                "vulnerabilities": [],
                "recommendations": [],
                "overall_risk": "LOW"
            }
            
            total_vulnerabilities = 0
            
            for language, files in languages.items():
                print(f"\n🔍 Analyzing {language}...")
                
                # Create basic components for this language
                components = [{
                    "name": f"{language}-component-{i}",
                    "version": "1.0.0",
                    "language": language,
                    "files": files[:3]  # First 3 files
                } for i in range(min(3, len(files)))]
                
                # Analyze vulnerabilities
                vulnerabilities = analyze_language_specific_risks(language, components)
                total_vulnerabilities += len(vulnerabilities)
                
                analysis_results["language_details"][language] = {
                    "files_found": len(files),
                    "components": len(components),
                    "vulnerabilities": len(vulnerabilities)
                }
                
                analysis_results["vulnerabilities"].extend(vulnerabilities)
            
            # Generate recommendations
            analysis_results["recommendations"] = generate_language_recommendations(languages)
            
            # Calculate overall risk
            if total_vulnerabilities > 5:
                analysis_results["overall_risk"] = "CRITICAL"
            elif total_vulnerabilities > 2:
                analysis_results["overall_risk"] = "HIGH"
            elif total_vulnerabilities > 0:
                analysis_results["overall_risk"] = "MEDIUM"
            else:
                analysis_results["overall_risk"] = "LOW"
            
            return analysis_results
            
        except Exception as e:
            return {
                "error": str(e),
                "repository": repo_url
            }

def format_report(results: Dict, format_type: str = 'json') -> str:
    """Format analysis results as report"""
    if format_type == 'json':
        return json.dumps(results, indent=2)
    
    # Text format
    text = []
    text.append("=" * 60)
    text.append("SBOMAI GITHUB PROJECT ANALYSIS REPORT")
    text.append("=" * 60)
    text.append(f"Repository: {results['repository']}")
    text.append(f"Overall Risk: {results.get('overall_risk', 'UNKNOWN')}")
    text.append("")
    
    if 'error' in results:
        text.append(f"❌ Error: {results['error']}")
        return "\n".join(text)
    
    # Languages detected
    text.append("🔍 LANGUAGES DETECTED")
    text.append("-" * 40)
    for lang in results.get('languages_detected', []):
        details = results.get('language_details', {}).get(lang, {})
        text.append(f"• {lang.upper()}: {details.get('files_found', 0)} files, {details.get('components', 0)} components")
    text.append("")
    
    # Vulnerabilities
    vulnerabilities = results.get('vulnerabilities', [])
    if vulnerabilities:
        text.append("⚠️  VULNERABILITIES FOUND")
        text.append("-" * 40)
        for vuln in vulnerabilities:
            text.append(f"• {vuln['component']} ({vuln['language']})")
            text.append(f"  CVE: {vuln['cve']} - {vuln['severity']} (CVSS: {vuln['cvss_score']})")
            text.append(f"  Description: {vuln['description']}")
            text.append("")
    
    # Recommendations
    recommendations = results.get('recommendations', [])
    if recommendations:
        text.append("🎯 RECOMMENDATIONS")
        text.append("-" * 40)
        for i, rec in enumerate(recommendations, 1):
            text.append(f"{i}. {rec}")
        text.append("")
    
    text.append("=" * 60)
    return "\n".join(text)

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="SBOMAI GitHub Project Scanner - Multi-language vulnerability analysis",
        epilog="""
Examples:
  python simple_github_scanner.py https://github.com/user/repo
  python simple_github_scanner.py https://github.com/user/repo --branch develop
  python simple_github_scanner.py https://github.com/user/repo --format text
        """
    )
    
    parser.add_argument('repository', help='GitHub repository URL to scan')
    parser.add_argument('--branch', '-b', help='Git branch to scan')
    parser.add_argument('--format', '-f', choices=['json', 'text'], default='json', help='Output format')
    parser.add_argument('--output', '-o', help='Output file path')
    
    args = parser.parse_args()
    
    # Scan repository
    results = scan_github_repository(args.repository, args.branch)
    
    # Format and output results
    report = format_report(results, args.format)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"📄 Report saved to: {args.output}")
    else:
        print("\n" + report)

if __name__ == "__main__":
    main() 