"""
Local transformer model integration for advanced analysis.
"""

from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    pipeline
)
from typing import List, Dict, Optional
import logging
from dataclasses import dataclass
import torch

logger = logging.getLogger(__name__)

@dataclass
class LocalTransformerConfig:
    """Configuration for local transformer models"""
    model_name: str = "microsoft/codebert-base"
    max_length: int = 512
    batch_size: int = 8
    device: str = "cuda" if torch.cuda.is_available() else "cpu"

class LocalTransformerModel:
    """
    Local transformer model integration for advanced vulnerability analysis.
    Uses HuggingFace transformers for local inference.
    """
    
    def __init__(self, config: LocalTransformerConfig):
        self.config = config
        
        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(config.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            config.model_name,
            num_labels=1  # Regression task
        ).to(config.device)
        
        # Create pipeline
        self.pipeline = pipeline(
            "text-classification",
            model=self.model,
            tokenizer=self.tokenizer,
            device=config.device
        )
    
    async def analyze_vulnerability(self, vuln_data: Dict) -> Dict:
        """
        Analyze vulnerability using local transformer model.
        
        Args:
            vuln_data: Vulnerability information
        
        Returns:
            Analysis results including:
            - Root cause analysis
            - Attack vector details
            - Remediation suggestions
            - Impact assessment
        """
        try:
            # Prepare input text
            input_text = self._prepare_input_text(vuln_data)
            
            # Get model predictions
            predictions = self.pipeline(
                input_text,
                max_length=self.config.max_length,
                truncation=True,
                batch_size=self.config.batch_size
            )
            
            # Parse predictions into analysis
            analysis = self._parse_predictions(predictions, vuln_data)
            
            return analysis
        
        except Exception as e:
            logger.error(f"Error in local transformer analysis: {e}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    def _prepare_input_text(self, vuln_data: Dict) -> str:
        """Prepare input text for model"""
        text = f"""
        Vulnerability Analysis Task:
        
        CVE: {vuln_data.get('cve_id', 'N/A')}
        Description: {vuln_data.get('description', '')}
        CVSS: {vuln_data.get('cvss_score', 0.0)}
        Vector: {vuln_data.get('cvss_vector', '')}
        
        Components:
        {self._format_components(vuln_data.get('affected_components', []))}
        
        Exploits:
        {self._format_exploits(vuln_data.get('known_exploits', []))}
        
        Analyze for:
        1. Root cause
        2. Attack vectors
        3. Remediation steps
        4. Impact assessment
        5. Security recommendations
        """
        return text
    
    def _format_components(self, components: List[Dict]) -> str:
        """Format affected components"""
        if not components:
            return "No specific components listed"
        
        return "\n".join(
            f"- {comp.get('name')}@{comp.get('version')}"
            for comp in components
        )
    
    def _format_exploits(self, exploits: List[Dict]) -> str:
        """Format known exploits"""
        if not exploits:
            return "No known exploits documented"
        
        return "\n".join(
            f"- {exp.get('type')}: {exp.get('description')}"
            for exp in exploits
        )
    
    def _parse_predictions(self, predictions: List[Dict], vuln_data: Dict) -> Dict:
        """Parse model predictions into analysis"""
        # Extract scores
        risk_score = float(predictions[0]["score"])
        
        # Create analysis structure
        analysis = {
            "root_cause": self._generate_root_cause(vuln_data, risk_score),
            "attack_vectors": self._generate_attack_vectors(vuln_data),
            "remediation": self._generate_remediation(vuln_data),
            "impact": self._generate_impact(vuln_data, risk_score),
            "recommendations": self._generate_recommendations(vuln_data)
        }
        
        return analysis
    
    def _generate_root_cause(self, vuln_data: Dict, risk_score: float) -> str:
        """Generate root cause analysis"""
        description = vuln_data.get('description', '')
        if not description:
            return "Insufficient information for root cause analysis"
        
        # Extract key phrases indicating root cause
        root_cause = "Based on the vulnerability description and analysis:\n"
        
        if "buffer" in description.lower():
            root_cause += "- Buffer overflow vulnerability\n"
        elif "sql" in description.lower():
            root_cause += "- SQL injection vulnerability\n"
        elif "xss" in description.lower():
            root_cause += "- Cross-site scripting vulnerability\n"
        elif "command" in description.lower():
            root_cause += "- Command injection vulnerability\n"
        else:
            root_cause += "- General security vulnerability\n"
        
        root_cause += f"Risk assessment score: {risk_score:.2f}"
        return root_cause
    
    def _generate_attack_vectors(self, vuln_data: Dict) -> List[str]:
        """Generate attack vector analysis"""
        vectors = []
        
        # Add known exploits
        for exploit in vuln_data.get('known_exploits', []):
            vectors.append(
                f"Known exploit: {exploit.get('type')} - "
                f"{exploit.get('description')}"
            )
        
        # Add potential vectors based on CVSS
        cvss_vector = vuln_data.get('cvss_vector', '')
        if 'AV:N' in cvss_vector:
            vectors.append("Network-based attack vector")
        if 'AC:L' in cvss_vector:
            vectors.append("Low complexity attack")
        if 'PR:N' in cvss_vector:
            vectors.append("No privileges required")
        
        return vectors if vectors else ["No specific attack vectors identified"]
    
    def _generate_remediation(self, vuln_data: Dict) -> List[str]:
        """Generate remediation steps"""
        steps = []
        
        # Check for available patches
        if vuln_data.get('fixed_version'):
            steps.append(
                f"Upgrade to fixed version: {vuln_data['fixed_version']}"
            )
        
        # Add general steps based on vulnerability type
        description = vuln_data.get('description', '').lower()
        
        if "buffer" in description:
            steps.extend([
                "Implement input validation",
                "Use safe string handling functions",
                "Enable compiler security flags"
            ])
        elif "sql" in description:
            steps.extend([
                "Use parameterized queries",
                "Implement input sanitization",
                "Review database access controls"
            ])
        elif "xss" in description:
            steps.extend([
                "Implement output encoding",
                "Use Content Security Policy",
                "Validate and sanitize user input"
            ])
        
        return steps if steps else ["No specific remediation steps available"]
    
    def _generate_impact(self, vuln_data: Dict, risk_score: float) -> str:
        """Generate impact assessment"""
        impact = f"Overall Risk Score: {risk_score:.2f}\n\n"
        
        # Add CVSS-based impact
        cvss = vuln_data.get('cvss_score', 0.0)
        impact += f"CVSS Score: {cvss}\n"
        
        if cvss >= 9.0:
            impact += "Critical severity - Immediate action required\n"
        elif cvss >= 7.0:
            impact += "High severity - Prioritize remediation\n"
        elif cvss >= 4.0:
            impact += "Medium severity - Plan remediation\n"
        else:
            impact += "Low severity - Monitor and review\n"
        
        # Add specific impacts
        cvss_vector = vuln_data.get('cvss_vector', '')
        if 'C:H' in cvss_vector:
            impact += "- High confidentiality impact\n"
        if 'I:H' in cvss_vector:
            impact += "- High integrity impact\n"
        if 'A:H' in cvss_vector:
            impact += "- High availability impact\n"
        
        return impact
    
    def _generate_recommendations(self, vuln_data: Dict) -> List[str]:
        """Generate security recommendations"""
        recs = []
        
        # Add general recommendations
        recs.extend([
            "Implement security monitoring",
            "Regular security assessments",
            "Update security policies"
        ])
        
        # Add specific recommendations based on vulnerability
        description = vuln_data.get('description', '').lower()
        
        if "authentication" in description:
            recs.extend([
                "Implement multi-factor authentication",
                "Review access control policies",
                "Audit authentication logs"
            ])
        elif "encryption" in description:
            recs.extend([
                "Review cryptographic implementations",
                "Update encryption protocols",
                "Implement key rotation"
            ])
        elif "configuration" in description:
            recs.extend([
                "Review security configurations",
                "Implement configuration management",
                "Regular configuration audits"
            ])
        
        return recs