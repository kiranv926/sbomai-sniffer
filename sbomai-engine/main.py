from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import json
import uuid
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="SBOMAI Engine API",
    description="AI/ML Engine for SBOM Analysis and Vulnerability Detection",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class VulnerabilityAnalysisRequest(BaseModel):
    scan_id: str
    sbom_content: Dict[str, Any]
    analysis_type: str = "comprehensive"

class VulnerabilityAnalysisResponse(BaseModel):
    scan_id: str
    analysis_id: str
    status: str
    vulnerabilities_found: int
    risk_score: float
    analysis_summary: Dict[str, Any]
    timestamp: datetime

class ComponentAnalysis(BaseModel):
    component_id: str
    name: str
    version: str
    vulnerabilities: List[Dict[str, Any]]
    risk_score: float

class AnalysisResult(BaseModel):
    scan_id: str
    components_analyzed: int
    vulnerabilities: List[Dict[str, Any]]
    risk_scores: Dict[str, float]
    recommendations: List[str]
    timestamp: datetime

# In-memory storage (replace with database in production)
analysis_results = {}

@app.get("/")
async def root():
    return {"message": "SBOMAI Engine API is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "sbomai-engine"
    }

@app.post("/api/v1/analyze-vulnerabilities", response_model=VulnerabilityAnalysisResponse)
async def analyze_vulnerabilities(request: VulnerabilityAnalysisRequest, background_tasks: BackgroundTasks):
    """Analyze SBOM for vulnerabilities using AI/ML models"""
    try:
        analysis_id = str(uuid.uuid4())
        
        # Start background analysis
        background_tasks.add_task(perform_vulnerability_analysis, analysis_id, request.scan_id, request.sbom_content)
        
        return VulnerabilityAnalysisResponse(
            scan_id=request.scan_id,
            analysis_id=analysis_id,
            status="processing",
            vulnerabilities_found=0,
            risk_score=0.0,
            analysis_summary={},
            timestamp=datetime.now()
        )
    except Exception as e:
        logger.error(f"Error starting vulnerability analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/analysis/{analysis_id}", response_model=AnalysisResult)
async def get_analysis_result(analysis_id: str):
    """Get analysis results by analysis ID"""
    if analysis_id not in analysis_results:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return analysis_results[analysis_id]

@app.get("/api/v1/scan/{scan_id}/analysis")
async def get_scan_analysis(scan_id: str):
    """Get analysis results by scan ID"""
    for analysis_id, result in analysis_results.items():
        if result.scan_id == scan_id:
            return result
    
    raise HTTPException(status_code=404, detail="Analysis not found for scan")

@app.post("/api/v1/upload-sbom")
async def upload_sbom(file: UploadFile = File(...)):
    """Upload SBOM file for analysis"""
    try:
        if not file.filename.endswith(('.json', '.xml')):
            raise HTTPException(status_code=400, detail="Only JSON and XML files are supported")
        
        content = await file.read()
        sbom_data = json.loads(content)
        
        scan_id = str(uuid.uuid4())
        
        return {
            "scan_id": scan_id,
            "filename": file.filename,
            "file_size": len(content),
            "components_count": len(sbom_data.get("components", [])),
            "upload_timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error uploading SBOM: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/models")
async def get_available_models():
    """Get list of available AI/ML models"""
    return {
        "models": [
            {
                "id": "vulnerability-detector",
                "name": "Vulnerability Detection Model",
                "type": "ml",
                "version": "1.0.0",
                "description": "Detects known vulnerabilities in software components"
            },
            {
                "id": "risk-analyzer",
                "name": "Risk Analysis Model",
                "type": "ai",
                "version": "1.0.0",
                "description": "Analyzes overall risk scores for components"
            },
            {
                "id": "dependency-analyzer",
                "name": "Dependency Analysis Model",
                "type": "ml",
                "version": "1.0.0",
                "description": "Analyzes dependency relationships and potential issues"
            }
        ]
    }

@app.get("/api/v1/statistics")
async def get_statistics():
    """Get analysis statistics"""
    total_analyses = len(analysis_results)
    completed_analyses = len([r for r in analysis_results.values() if r.status == "completed"])
    
    return {
        "total_analyses": total_analyses,
        "completed_analyses": completed_analyses,
        "pending_analyses": total_analyses - completed_analyses,
        "average_risk_score": 0.0,  # Calculate from actual data
        "timestamp": datetime.now().isoformat()
    }

async def perform_vulnerability_analysis(analysis_id: str, scan_id: str, sbom_content: Dict[str, Any]):
    """Background task to perform vulnerability analysis"""
    try:
        logger.info(f"Starting vulnerability analysis for scan {scan_id}")
        
        # Simulate analysis processing time
        import asyncio
        await asyncio.sleep(5)
        
        # Mock analysis results
        components = sbom_content.get("components", [])
        vulnerabilities = []
        risk_scores = {}
        
        for component in components:
            comp_name = component.get("name", "unknown")
            comp_version = component.get("version", "unknown")
            comp_id = f"{comp_name}@{comp_version}"
            
            # Mock vulnerability detection
            if "log4j" in comp_name.lower():
                vulnerabilities.append({
                    "id": "CVE-2021-44228",
                    "component": comp_id,
                    "severity": "critical",
                    "description": "Log4j vulnerability",
                    "cvss_score": 10.0,
                    "cve_id": "CVE-2021-44228"
                })
                risk_scores[comp_id] = 0.9
            else:
                risk_scores[comp_id] = 0.1
        
        # Create analysis result
        result = AnalysisResult(
            scan_id=scan_id,
            components_analyzed=len(components),
            vulnerabilities=vulnerabilities,
            risk_scores=risk_scores,
            recommendations=[
                "Update log4j to version 2.17.0 or later",
                "Consider using alternative logging frameworks",
                "Implement security scanning in CI/CD pipeline"
            ],
            timestamp=datetime.now()
        )
        
        analysis_results[analysis_id] = result
        logger.info(f"Vulnerability analysis completed for scan {scan_id}")
        
    except Exception as e:
        logger.error(f"Error in vulnerability analysis: {e}")
        # Store error result
        analysis_results[analysis_id] = AnalysisResult(
            scan_id=scan_id,
            components_analyzed=0,
            vulnerabilities=[],
            risk_scores={},
            recommendations=[],
            timestamp=datetime.now()
        )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
