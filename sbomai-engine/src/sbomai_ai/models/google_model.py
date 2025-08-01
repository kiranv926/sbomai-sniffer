"""
Google Gemini model integration for advanced analysis.
"""

import google.generativeai as genai
from typing import List, Dict, Optional
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class GoogleGeminiConfig:
    """Configuration for Google Gemini models"""
    api_key: str
    model: str = "gemini-pro"
    temperature: float = 0.7
    max_output_tokens: int = 1000

class GoogleGeminiModel:
    """
    Google Gemini model integration for advanced vulnerability analysis.
    """
    
    def __init__(self, config: GoogleGeminiConfig):
        self.config = config
        genai.configure(api_key=config.api_key)
        self.model = genai.GenerativeModel(
            model_name=config.model,
            generation_config={
                "temperature": config.temperature,
                "max_output_tokens": config.max_output_tokens
            }
        )
    
    async def analyze_vulnerability(self, vuln_data: Dict) -> Dict:
        """
        Analyze vulnerability using Google Gemini.
        
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
            response = await self.model.generate_content_async(prompt)
            
            # Parse response
            analysis = self._parse_analysis_response(
                response.text
            )
            
            return analysis
        
        except Exception as e:
            logger.error(f"Error in Gemini analysis: {e}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    def _create_analysis_prompt(self, vuln_data: Dict) -> str:
        """Create analysis prompt from vulnerability data"""
        prompt = f"""
        As a security expert, analyze this vulnerability:
        
        CVE ID: {vuln_data.get('cve_id', 'N/A')}
        Description: {vuln_data.get('description', '')}
        CVSS Score: {vuln_data.get('cvss_score', 0.0)}
        CVSS Vector: {vuln_data.get('cvss_vector', '')}
        
        Affected Components:
        {self._format_components(vuln_data.get('affected_components', []))}
        
        Known Exploits:
        {self._format_exploits(vuln_data.get('known_exploits', []))}
        
        Please provide a comprehensive security analysis with these sections:
        
        1. Root Cause Analysis
        - Identify the fundamental vulnerability
        - Explain the technical details
        - Highlight any architectural issues
        
        2. Attack Vectors
        - List all possible exploitation methods
        - Detail the attack prerequisites
        - Describe potential attack scenarios
        
        3. Remediation Steps
        - Provide specific patching instructions
        - List configuration changes needed
        - Suggest compensating controls
        
        4. Impact Assessment
        - Analyze potential business impact
        - Evaluate data exposure risks
        - Consider operational effects
        
        5. Security Recommendations
        - Suggest long-term security improvements
        - Recommend monitoring approaches
        - Propose architectural enhancements
        
        Format your response with clear section headers and bullet points.
        Focus on actionable, technical details that security teams can implement.
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
        """Parse Gemini response into structured analysis"""
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