"""
Anthropic Claude model integration for advanced analysis.
"""

import anthropic
from typing import List, Dict, Optional
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class AnthropicConfig:
    """Configuration for Anthropic models"""
    api_key: str
    model: str = "claude-2"
    max_tokens: int = 1000
    temperature: float = 0.7

class AnthropicModel:
    """
    Anthropic Claude model integration for advanced vulnerability analysis.
    """
    
    def __init__(self, config: AnthropicConfig):
        self.config = config
        self.client = anthropic.Client(api_key=config.api_key)
    
    async def analyze_vulnerability(self, vuln_data: Dict) -> Dict:
        """
        Analyze vulnerability using Anthropic Claude.
        
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
            response = await self.client.messages.create(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Parse response
            analysis = self._parse_analysis_response(
                response.content[0].text
            )
            
            return analysis
        
        except Exception as e:
            logger.error(f"Error in Anthropic analysis: {e}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    def _create_analysis_prompt(self, vuln_data: Dict) -> str:
        """Create analysis prompt from vulnerability data"""
        prompt = f"""
        Analyze this vulnerability as a security expert:
        
        CVE ID: {vuln_data.get('cve_id', 'N/A')}
        Description: {vuln_data.get('description', '')}
        CVSS Score: {vuln_data.get('cvss_score', 0.0)}
        CVSS Vector: {vuln_data.get('cvss_vector', '')}
        
        Affected Components:
        {self._format_components(vuln_data.get('affected_components', []))}
        
        Known Exploits:
        {self._format_exploits(vuln_data.get('known_exploits', []))}
        
        Please provide a detailed analysis including:
        1. Root cause analysis - What is the fundamental vulnerability?
        2. Attack vectors - How can this vulnerability be exploited?
        3. Remediation steps - What specific actions should be taken?
        4. Impact assessment - What are the potential consequences?
        5. Security recommendations - What additional measures should be implemented?
        
        Format your response with clear sections and bullet points where appropriate.
        Focus on actionable, technical details.
        """
        return prompt
    
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
        """Parse Claude response into structured analysis"""
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
            if section.lower().startswith("root cause"):
                current_section = "root_cause"
                analysis["root_cause"] = section.split(":", 1)[1].strip()
            
            elif section.lower().startswith("attack vector"):
                current_section = "attack_vectors"
                vectors = section.split("\n")[1:]
                analysis["attack_vectors"].extend(
                    v.strip("- ") for v in vectors if v.strip()
                )
            
            elif section.lower().startswith("remediation"):
                current_section = "remediation"
                steps = section.split("\n")[1:]
                analysis["remediation"].extend(
                    s.strip("- ") for s in steps if s.strip()
                )
            
            elif section.lower().startswith("impact"):
                current_section = "impact"
                analysis["impact"] = section.split(":", 1)[1].strip()
            
            elif section.lower().startswith("recommendation"):
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