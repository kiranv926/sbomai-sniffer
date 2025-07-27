"""
Explainability models using LangChain for SBOM analysis
"""

import asyncio
import time
from typing import Dict, List, Optional, Any
import logging

from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains.question_answering import load_qa_chain

from ..config import get_config
from ..utils.exceptions import ExplainabilityError
from .ai_models import AiModelFactory

logger = logging.getLogger(__name__)


class SbomAnalysisParser(BaseOutputParser):
    """Parser for SBOM analysis outputs"""
    
    def parse(self, text: str) -> Dict[str, Any]:
        """Parse the analysis output into structured format"""
        try:
            # Simple parsing - in practice, you'd use more sophisticated parsing
            lines = text.strip().split('\n')
            result = {
                "risk_level": "MEDIUM",
                "risk_score": 5.0,
                "key_findings": [],
                "recommendations": [],
                "confidence": 0.7
            }
            
            for line in lines:
                line = line.strip()
                if "risk level:" in line.lower():
                    if "critical" in line.lower():
                        result["risk_level"] = "CRITICAL"
                    elif "high" in line.lower():
                        result["risk_level"] = "HIGH"
                    elif "low" in line.lower():
                        result["risk_level"] = "LOW"
                elif "risk score:" in line.lower():
                    try:
                        score = float(line.split(":")[-1].strip())
                        result["risk_score"] = min(max(score, 0), 10)
                    except:
                        pass
                elif "finding:" in line.lower() or "issue:" in line.lower():
                    finding = line.split(":", 1)[-1].strip()
                    if finding:
                        result["key_findings"].append(finding)
                elif "recommendation:" in line.lower() or "suggestion:" in line.lower():
                    rec = line.split(":", 1)[-1].strip()
                    if rec:
                        result["recommendations"].append(rec)
            
            return result
        except Exception as e:
            logger.warning(f"Failed to parse analysis output: {e}")
            return {
                "risk_level": "UNKNOWN",
                "risk_score": 5.0,
                "key_findings": ["Analysis parsing failed"],
                "recommendations": ["Review manually"],
                "confidence": 0.3
            }


class ExplainabilityChain:
    """LangChain-based explainable analysis chain for SBOM"""
    
    def __init__(self):
        self.config = get_config()
        self.ai_model = None
        self.chains = {}
        self.memory = ConversationBufferMemory()
        self._initialize_chains()
    
    def _initialize_chains(self):
        """Initialize LangChain analysis chains"""
        try:
            # Get the best available AI model
            self.ai_model = AiModelFactory.get_best_available_model()
            if not self.ai_model:
                raise ExplainabilityError("No AI model available for explainability chain")
            
            # Create analysis chains
            self._create_vulnerability_analysis_chain()
            self._create_license_analysis_chain()
            self._create_outdated_component_chain()
            self._create_overall_assessment_chain()
            
            logger.info("Explainability chains initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize explainability chains: {e}")
            raise ExplainabilityError(f"Chain initialization failed: {e}")
    
    def _create_vulnerability_analysis_chain(self):
        """Create vulnerability analysis chain"""
        vulnerability_template = """
        Analyze the following SBOM component for security vulnerabilities:
        
        Component: {component_name} {component_version}
        Description: {component_description}
        Vulnerabilities: {vulnerabilities}
        
        Provide a detailed analysis including:
        1. Risk Level (LOW/MEDIUM/HIGH/CRITICAL)
        2. Risk Score (0-10)
        3. Key Findings (list specific issues)
        4. Recommendations (actionable steps)
        5. Confidence Level (0-1)
        
        Analysis:
        """
        
        prompt = PromptTemplate(
            input_variables=["component_name", "component_version", "component_description", "vulnerabilities"],
            template=vulnerability_template
        )
        
        self.chains["vulnerability"] = LLMChain(
            llm=self._get_langchain_llm(),
            prompt=prompt,
            output_parser=SbomAnalysisParser(),
            memory=self.memory
        )
    
    def _create_license_analysis_chain(self):
        """Create license analysis chain"""
        license_template = """
        Analyze the license compliance for the following SBOM component:
        
        Component: {component_name} {component_version}
        Licenses: {licenses}
        Project Context: {project_context}
        
        Provide analysis including:
        1. License Risk Level (LOW/MEDIUM/HIGH/CRITICAL)
        2. Compliance Status
        3. Key License Issues
        4. Recommendations
        5. Confidence Level (0-1)
        
        Analysis:
        """
        
        prompt = PromptTemplate(
            input_variables=["component_name", "component_version", "licenses", "project_context"],
            template=license_template
        )
        
        self.chains["license"] = LLMChain(
            llm=self._get_langchain_llm(),
            prompt=prompt,
            output_parser=SbomAnalysisParser(),
            memory=self.memory
        )
    
    def _create_outdated_component_chain(self):
        """Create outdated component analysis chain"""
        outdated_template = """
        Analyze if the following SBOM component is outdated:
        
        Component: {component_name} {component_version}
        Latest Version: {latest_version}
        Release Date: {release_date}
        Update Frequency: {update_frequency}
        
        Provide analysis including:
        1. Outdated Risk Level (LOW/MEDIUM/HIGH/CRITICAL)
        2. Age Assessment
        3. Security Implications
        4. Update Recommendations
        5. Confidence Level (0-1)
        
        Analysis:
        """
        
        prompt = PromptTemplate(
            input_variables=["component_name", "component_version", "latest_version", "release_date", "update_frequency"],
            template=outdated_template
        )
        
        self.chains["outdated"] = LLMChain(
            llm=self._get_langchain_llm(),
            prompt=prompt,
            output_parser=SbomAnalysisParser(),
            memory=self.memory
        )
    
    def _create_overall_assessment_chain(self):
        """Create overall SBOM assessment chain"""
        overall_template = """
        Provide an overall assessment of the SBOM based on the following analysis results:
        
        Vulnerability Analysis: {vulnerability_analysis}
        License Analysis: {license_analysis}
        Outdated Component Analysis: {outdated_analysis}
        
        Component Summary:
        - Total Components: {total_components}
        - High Risk Components: {high_risk_count}
        - Critical Vulnerabilities: {critical_vuln_count}
        - License Violations: {license_violations}
        
        Provide overall assessment including:
        1. Overall Risk Level
        2. Overall Risk Score (0-10)
        3. Critical Findings Summary
        4. Priority Recommendations
        5. Confidence Level (0-1)
        
        Overall Assessment:
        """
        
        prompt = PromptTemplate(
            input_variables=[
                "vulnerability_analysis", "license_analysis", "outdated_analysis",
                "total_components", "high_risk_count", "critical_vuln_count", "license_violations"
            ],
            template=overall_template
        )
        
        self.chains["overall"] = LLMChain(
            llm=self._get_langchain_llm(),
            prompt=prompt,
            output_parser=SbomAnalysisParser(),
            memory=self.memory
        )
    
    def _get_langchain_llm(self):
        """Get LangChain LLM wrapper for our AI model"""
        # This is a simplified wrapper - in practice, you'd create a proper LangChain LLM
        class CustomLLM:
            def __init__(self, ai_model):
                self.ai_model = ai_model
            
            async def agenerate(self, prompts, **kwargs):
                results = []
                for prompt in prompts:
                    response = await self.ai_model.generate_response(prompt[0])
                    results.append([response])
                return {"generations": results}
        
        return CustomLLM(self.ai_model)
    
    async def analyze_component_vulnerabilities(self, component: Dict[str, Any], vulnerabilities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze component vulnerabilities"""
        try:
            vuln_text = "\n".join([
                f"- {v.get('id', 'Unknown')}: {v.get('description', 'No description')} (CVSS: {v.get('cvss_score', 'Unknown')})"
                for v in vulnerabilities
            ])
            
            result = await self.chains["vulnerability"].arun({
                "component_name": component.get("name", "Unknown"),
                "component_version": component.get("version", "Unknown"),
                "component_description": component.get("description", "No description"),
                "vulnerabilities": vuln_text or "No known vulnerabilities"
            })
            
            return result
        except Exception as e:
            logger.error(f"Vulnerability analysis failed: {e}")
            raise ExplainabilityError(f"Vulnerability analysis failed: {e}")
    
    async def analyze_component_licenses(self, component: Dict[str, Any], project_context: str = "") -> Dict[str, Any]:
        """Analyze component licenses"""
        try:
            licenses = component.get("licenses", [])
            license_text = ", ".join(licenses) if licenses else "No license information"
            
            result = await self.chains["license"].arun({
                "component_name": component.get("name", "Unknown"),
                "component_version": component.get("version", "Unknown"),
                "licenses": license_text,
                "project_context": project_context or "General software project"
            })
            
            return result
        except Exception as e:
            logger.error(f"License analysis failed: {e}")
            raise ExplainabilityError(f"License analysis failed: {e}")
    
    async def analyze_outdated_component(self, component: Dict[str, Any], latest_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze if component is outdated"""
        try:
            result = await self.chains["outdated"].arun({
                "component_name": component.get("name", "Unknown"),
                "component_version": component.get("version", "Unknown"),
                "latest_version": latest_info.get("latest_version", "Unknown"),
                "release_date": latest_info.get("release_date", "Unknown"),
                "update_frequency": latest_info.get("update_frequency", "Unknown")
            })
            
            return result
        except Exception as e:
            logger.error(f"Outdated component analysis failed: {e}")
            raise ExplainabilityError(f"Outdated component analysis failed: {e}")
    
    async def generate_overall_assessment(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate overall SBOM assessment"""
        try:
            result = await self.chains["overall"].arun({
                "vulnerability_analysis": str(analysis_results.get("vulnerability_analysis", {})),
                "license_analysis": str(analysis_results.get("license_analysis", {})),
                "outdated_analysis": str(analysis_results.get("outdated_analysis", {})),
                "total_components": analysis_results.get("total_components", 0),
                "high_risk_count": analysis_results.get("high_risk_count", 0),
                "critical_vuln_count": analysis_results.get("critical_vuln_count", 0),
                "license_violations": analysis_results.get("license_violations", 0)
            })
            
            return result
        except Exception as e:
            logger.error(f"Overall assessment failed: {e}")
            raise ExplainabilityError(f"Overall assessment failed: {e}")


class LangChainAnalyzer:
    """Main LangChain-based analyzer for SBOM explainability"""
    
    def __init__(self):
        self.config = get_config()
        self.explainability_chain = None
        self.vector_store = None
        self._initialize_analyzer()
    
    def _initialize_analyzer(self):
        """Initialize the LangChain analyzer"""
        try:
            self.explainability_chain = ExplainabilityChain()
            
            # Initialize vector store for similarity search (optional)
            if self.config.features.get("vector_search", False):
                self._initialize_vector_store()
            
            logger.info("LangChain analyzer initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize LangChain analyzer: {e}")
            raise ExplainabilityError(f"Analyzer initialization failed: {e}")
    
    def _initialize_vector_store(self):
        """Initialize vector store for similarity search"""
        try:
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
            
            # Create empty vector store - in practice, you'd load existing knowledge
            self.vector_store = FAISS.from_texts(
                ["Initial document"],
                embeddings
            )
            
            logger.info("Vector store initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize vector store: {e}")
            self.vector_store = None
    
    async def explain_risk(self, component: Dict[str, Any], vulnerabilities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Explain risk for a specific component"""
        try:
            start_time = time.time()
            
            # Analyze vulnerabilities
            vuln_analysis = await self.explainability_chain.analyze_component_vulnerabilities(
                component, vulnerabilities
            )
            
            # Analyze licenses
            license_analysis = await self.explainability_chain.analyze_component_licenses(component)
            
            # Get latest version info (simulated)
            latest_info = {
                "latest_version": "2.0.0",
                "release_date": "2024-01-15",
                "update_frequency": "Monthly"
            }
            
            # Analyze if outdated
            outdated_analysis = await self.explainability_chain.analyze_outdated_component(
                component, latest_info
            )
            
            processing_time = (time.time() - start_time) * 1000
            
            return {
                "component": component,
                "vulnerability_analysis": vuln_analysis,
                "license_analysis": license_analysis,
                "outdated_analysis": outdated_analysis,
                "processing_time_ms": int(processing_time),
                "model_used": self.explainability_chain.ai_model.model_name
            }
            
        except Exception as e:
            logger.error(f"Risk explanation failed: {e}")
            raise ExplainabilityError(f"Risk explanation failed: {e}")
    
    async def explain_sbom_chain(self, sbom_document: Dict[str, Any]) -> Dict[str, Any]:
        """Generate explainable analysis chain for entire SBOM"""
        try:
            start_time = time.time()
            
            components = sbom_document.get("components", [])
            analysis_results = {
                "total_components": len(components),
                "high_risk_count": 0,
                "critical_vuln_count": 0,
                "license_violations": 0,
                "component_analyses": []
            }
            
            # Analyze each component
            for component in components:
                # Simulate vulnerabilities for demo
                vulnerabilities = [
                    {
                        "id": "CVE-2024-0001",
                        "description": "Example vulnerability",
                        "cvss_score": 7.5
                    }
                ] if component.get("name") == "example-library" else []
                
                component_analysis = await self.explain_risk(component, vulnerabilities)
                analysis_results["component_analyses"].append(component_analysis)
                
                # Count high-risk components
                if component_analysis["vulnerability_analysis"].get("risk_level") in ["HIGH", "CRITICAL"]:
                    analysis_results["high_risk_count"] += 1
                
                if component_analysis["vulnerability_analysis"].get("risk_level") == "CRITICAL":
                    analysis_results["critical_vuln_count"] += 1
            
            # Generate overall assessment
            overall_assessment = await self.explainability_chain.generate_overall_assessment(analysis_results)
            
            processing_time = (time.time() - start_time) * 1000
            
            return {
                "sbom_document": sbom_document,
                "overall_assessment": overall_assessment,
                "component_analyses": analysis_results["component_analyses"],
                "summary": {
                    "total_components": analysis_results["total_components"],
                    "high_risk_count": analysis_results["high_risk_count"],
                    "critical_vuln_count": analysis_results["critical_vuln_count"],
                    "license_violations": analysis_results["license_violations"]
                },
                "processing_time_ms": int(processing_time),
                "model_used": self.explainability_chain.ai_model.model_name
            }
            
        except Exception as e:
            logger.error(f"SBOM chain analysis failed: {e}")
            raise ExplainabilityError(f"SBOM chain analysis failed: {e}")
    
    async def suggest_remediation(self, vulnerability_id: str, component: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest remediation for a specific vulnerability"""
        try:
            # Create remediation suggestion chain
            remediation_template = """
            Suggest remediation for the following vulnerability:
            
            Vulnerability ID: {vulnerability_id}
            Component: {component_name} {component_version}
            Description: {component_description}
            
            Provide remediation suggestions including:
            1. Immediate Actions
            2. Alternative Components
            3. Version Updates
            4. Security Measures
            5. Confidence Level (0-1)
            
            Remediation Suggestions:
            """
            
            prompt = PromptTemplate(
                input_variables=["vulnerability_id", "component_name", "component_version", "component_description"],
                template=remediation_template
            )
            
            chain = LLMChain(
                llm=self.explainability_chain._get_langchain_llm(),
                prompt=prompt,
                output_parser=SbomAnalysisParser()
            )
            
            result = await chain.arun({
                "vulnerability_id": vulnerability_id,
                "component_name": component.get("name", "Unknown"),
                "component_version": component.get("version", "Unknown"),
                "component_description": component.get("description", "No description")
            })
            
            return {
                "vulnerability_id": vulnerability_id,
                "component": component,
                "remediation_suggestions": result,
                "model_used": self.explainability_chain.ai_model.model_name
            }
            
        except Exception as e:
            logger.error(f"Remediation suggestion failed: {e}")
            raise ExplainabilityError(f"Remediation suggestion failed: {e}")
    
    def get_analyzer_info(self) -> Dict[str, Any]:
        """Get analyzer information"""
        return {
            "name": "LangChain SBOM Analyzer",
            "version": "1.0.0",
            "capabilities": [
                "explain_risk",
                "explain_sbom_chain", 
                "suggest_remediation",
                "vector_search"
            ],
            "ai_model": self.explainability_chain.ai_model.get_model_info() if self.explainability_chain else None,
            "vector_store_available": self.vector_store is not None
        } 