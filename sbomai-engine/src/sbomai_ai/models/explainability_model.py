"""
Explainability Chain model for vulnerability analysis.
"""

from typing import List, Dict, Optional, Tuple
import logging
from dataclasses import dataclass
import numpy as np
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import OpenAI, Anthropic
import shap

logger = logging.getLogger(__name__)

@dataclass
class ExplainabilityConfig:
    """Configuration for Explainability Chain"""
    llm_type: str = "openai"  # or "anthropic"
    api_key: Optional[str] = None
    model_name: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 1000

class ExplainabilityChain:
    """
    LangChain-based explainability model for vulnerability analysis.
    """
    
    def __init__(self, config: ExplainabilityConfig):
        self.config = config
        
        # Initialize LLM
        if config.llm_type == "openai":
            self.llm = OpenAI(
                api_key=config.api_key,
                model_name=config.model_name or "gpt-4",
                temperature=config.temperature,
                max_tokens=config.max_tokens
            )
        elif config.llm_type == "anthropic":
            self.llm = Anthropic(
                api_key=config.api_key,
                model=config.model_name or "claude-2",
                temperature=config.temperature,
                max_tokens=config.max_tokens
            )
        else:
            raise ValueError(f"Unsupported LLM type: {config.llm_type}")
        
        # Initialize chains
        self.chains = self._create_chains()
    
    def _create_chains(self) -> Dict[str, LLMChain]:
        """Create LangChain chains for different analysis aspects"""
        chains = {}
        
        # Root cause analysis chain
        root_cause_template = """
        Analyze the root cause of this vulnerability:
        
        CVE: {cve_id}
        Description: {description}
        Affected Components: {components}
        
        Provide a detailed technical explanation of:
        1. The fundamental vulnerability
        2. The affected code patterns
        3. The architectural implications
        4. The security design flaws
        
        Format your response with clear sections and technical details.
        """
        
        chains['root_cause'] = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(
                input_variables=[
                    "cve_id",
                    "description",
                    "components"
                ],
                template=root_cause_template
            )
        )
        
        # Attack vector analysis chain
        attack_vector_template = """
        Analyze the attack vectors for this vulnerability:
        
        CVE: {cve_id}
        Description: {description}
        Known Exploits: {exploits}
        
        Provide a detailed analysis of:
        1. Possible attack methods
        2. Required attacker capabilities
        3. Potential attack scenarios
        4. Attack complexity factors
        
        Format your response with clear sections and technical details.
        """
        
        chains['attack_vectors'] = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(
                input_variables=[
                    "cve_id",
                    "description",
                    "exploits"
                ],
                template=attack_vector_template
            )
        )
        
        # Impact analysis chain
        impact_template = """
        Analyze the potential impact of this vulnerability:
        
        CVE: {cve_id}
        Description: {description}
        CVSS Score: {cvss_score}
        CVSS Vector: {cvss_vector}
        
        Provide a detailed analysis of:
        1. Technical impact
        2. Business impact
        3. Data exposure risks
        4. Operational effects
        
        Format your response with clear sections and impact severity levels.
        """
        
        chains['impact'] = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(
                input_variables=[
                    "cve_id",
                    "description",
                    "cvss_score",
                    "cvss_vector"
                ],
                template=impact_template
            )
        )
        
        # Remediation analysis chain
        remediation_template = """
        Provide remediation guidance for this vulnerability:
        
        CVE: {cve_id}
        Description: {description}
        Available Patches: {patches}
        
        Provide detailed recommendations for:
        1. Immediate mitigation steps
        2. Long-term fixes
        3. Configuration changes
        4. Security control improvements
        
        Format your response with clear, actionable steps.
        """
        
        chains['remediation'] = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(
                input_variables=[
                    "cve_id",
                    "description",
                    "patches"
                ],
                template=remediation_template
            )
        )
        
        return chains
    
    async def analyze_vulnerability(self, vuln_data: Dict) -> Dict:
        """
        Generate comprehensive explainability analysis.
        
        Args:
            vuln_data: Vulnerability information
        
        Returns:
            Analysis results including:
            - Root cause explanation
            - Attack vector analysis
            - Impact assessment
            - Remediation guidance
        """
        try:
            # Prepare chain inputs
            root_cause_input = {
                "cve_id": vuln_data.get('cve_id', 'N/A'),
                "description": vuln_data.get('description', ''),
                "components": self._format_components(
                    vuln_data.get('affected_components', [])
                )
            }
            
            attack_vector_input = {
                "cve_id": vuln_data.get('cve_id', 'N/A'),
                "description": vuln_data.get('description', ''),
                "exploits": self._format_exploits(
                    vuln_data.get('known_exploits', [])
                )
            }
            
            impact_input = {
                "cve_id": vuln_data.get('cve_id', 'N/A'),
                "description": vuln_data.get('description', ''),
                "cvss_score": vuln_data.get('cvss_score', 0.0),
                "cvss_vector": vuln_data.get('cvss_vector', '')
            }
            
            remediation_input = {
                "cve_id": vuln_data.get('cve_id', 'N/A'),
                "description": vuln_data.get('description', ''),
                "patches": self._format_patches(
                    vuln_data.get('available_patches', [])
                )
            }
            
            # Run chains
            root_cause = await self.chains['root_cause'].arun(**root_cause_input)
            attack_vectors = await self.chains['attack_vectors'].arun(**attack_vector_input)
            impact = await self.chains['impact'].arun(**impact_input)
            remediation = await self.chains['remediation'].arun(**remediation_input)
            
            # Combine results
            analysis = {
                "root_cause_analysis": self._parse_section(root_cause),
                "attack_vector_analysis": self._parse_section(attack_vectors),
                "impact_assessment": self._parse_section(impact),
                "remediation_guidance": self._parse_section(remediation)
            }
            
            return analysis
        
        except Exception as e:
            logger.error(f"Error in explainability analysis: {e}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    def _format_components(self, components: List[Dict]) -> str:
        """Format component information for prompt"""
        if not components:
            return "No specific components listed"
        
        return "\n".join(
            f"- {comp.get('name')}@{comp.get('version')}"
            for comp in components
        )
    
    def _format_exploits(self, exploits: List[Dict]) -> str:
        """Format exploit information for prompt"""
        if not exploits:
            return "No known exploits documented"
        
        return "\n".join(
            f"- {exp.get('type')}: {exp.get('description')}"
            for exp in exploits
        )
    
    def _format_patches(self, patches: List[Dict]) -> str:
        """Format patch information for prompt"""
        if not patches:
            return "No specific patches available"
        
        return "\n".join(
            f"- {patch.get('id')}: {patch.get('description')}"
            for patch in patches
        )
    
    def _parse_section(self, text: str) -> Dict:
        """Parse section text into structured format"""
        lines = text.strip().split("\n")
        
        section = {
            "summary": "",
            "details": [],
            "recommendations": []
        }
        
        current_part = "summary"
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.lower().startswith(("recommend", "suggest")):
                current_part = "recommendations"
                section["recommendations"].append(
                    line.split(":", 1)[1].strip()
                    if ":" in line
                    else line
                )
            elif line.startswith("-") or line.startswith("*"):
                if current_part == "summary":
                    current_part = "details"
                section["details"].append(line.lstrip("- *").strip())
            elif not section["summary"]:
                section["summary"] = line
            else:
                section["details"].append(line)
        
        return section