"""
OpenAI model integration for advanced analysis.
"""

import openai
from typing import List, Dict, Optional
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class OpenAiConfig:
    """Configuration for OpenAI models"""
    api_key: str
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 1000

class OpenAiModel:
    """
    OpenAI model integration for advanced vulnerability analysis.
    """
    
    def __init__(self, config: OpenAiConfig):
        self.config = config
        openai.api_key = config.api_key
    
    async def analyze_vulnerability(self, vuln_data: Dict) -> Dict:
        """
        Analyze vulnerability using OpenAI model.
        
        Args:
            vuln_data: Vulnerability information
        
        Returns:
            Analysis results including:
            - Root cause analysis
            - Attack vector details
            - Remediation suggestions
            - Impact assessment
        """
        # Create prompt
        prompt = self._create_analysis_prompt(vuln_data)
        
        try:
            # Get completion
            response = await openai.ChatCompletion.acreate(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            # Parse response
            analysis = self._parse_analysis_response(
                response.choices[0].message.content
            )
            
            return analysis
        
        except Exception as e:
            logger.error(f"Error in OpenAI analysis: {e}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    def _create_analysis_prompt(self, vuln_data: Dict) -> str:
        """Create analysis prompt from vulnerability data"""
        prompt = f"""
        Analyze this vulnerability:
        
        CVE ID: {vuln_data.get('cve_id', 'N/A')}
        Description: {vuln_data.get('description', '')}
        CVSS Score: {vuln_data.get('cvss_score', 0.0)}
        CVSS Vector: {vuln_data.get('cvss_vector', '')}
        
        Affected Components:
        {self._format_components(vuln_data.get('affected_components', []))}
        
        Known Exploits:
        {self._format_exploits(vuln_data.get('known_exploits', []))}
        
        Provide:
        1. Root cause analysis
        2. Detailed attack vectors
        3. Specific remediation steps
        4. Impact assessment
        5. Additional security recommendations
        """
        return prompt
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for analysis"""
        return """
        You are an expert vulnerability analyst with deep knowledge of:
        - Software security
        - Exploit development
        - Security architecture
        - Risk assessment
        - Remediation strategies
        
        Analyze vulnerabilities and provide detailed, actionable insights.
        Focus on practical, implementable recommendations.
        Include specific technical details where relevant.
        """
    
    def _format_components(self, components: List[Dict]) -> str:
        """Format affected components for prompt"""
        if not components:
            return "No specific components listed"
        
        return "\n".join(
            f"- {comp.get('name')}@{comp.get('version')}"
            for comp in components
        )
    
    def _format_exploits(self, exploits: List[Dict]) -> str:
        """Format known exploits for prompt"""
        if not exploits:
            return "No known exploits documented"
        
        return "\n".join(
            f"- {exp.get('type')}: {exp.get('description')}"
            for exp in exploits
        )
    
    def _parse_analysis_response(self, response: str) -> Dict:
        """Parse OpenAI response into structured analysis"""
        # Split response into sections
        sections = response.split("\n\n")
        
        analysis = {
            "root_cause": "",
            "attack_vectors": [],
            "remediation": [],
            "impact": "",
            "recommendations": []
        }
        
        current_section = None
        for section in sections:
            section = section.strip()
            if not section:
                continue
            
            # Identify section
            if section.startswith("Root cause"):
                current_section = "root_cause"
                analysis["root_cause"] = section.split(":", 1)[1].strip()
            
            elif section.startswith("Attack vector"):
                current_section = "attack_vectors"
                vectors = section.split("\n")[1:]
                analysis["attack_vectors"].extend(
                    v.strip("- ") for v in vectors if v.strip()
                )
            
            elif section.startswith("Remediation"):
                current_section = "remediation"
                steps = section.split("\n")[1:]
                analysis["remediation"].extend(
                    s.strip("- ") for s in steps if s.strip()
                )
            
            elif section.startswith("Impact"):
                current_section = "impact"
                analysis["impact"] = section.split(":", 1)[1].strip()
            
            elif section.startswith("Recommendation"):
                current_section = "recommendations"
                recs = section.split("\n")[1:]
                analysis["recommendations"].extend(
                    r.strip("- ") for r in recs if r.strip()
                )
            
            # Add content to current section
            elif current_section:
                if current_section in ["attack_vectors", "remediation", "recommendations"]:
                    analysis[current_section].extend(
                        line.strip("- ")
                        for line in section.split("\n")
                        if line.strip()
                    )
                else:
                    analysis[current_section] += "\n" + section
        
        return analysis