"""
SBOMAI AI service implementation.
"""

import logging
import asyncio
from typing import List, Dict, Optional, AsyncGenerator
import grpc
from concurrent import futures

from .models import (
    OpenAiModel, OpenAiConfig,
    AnthropicModel, AnthropicConfig,
    GoogleGeminiModel, GoogleGeminiConfig,
    LocalTransformerModel, LocalTransformerConfig,
    XGBoostRiskModel, XGBoostConfig,
    LightGBMRiskModel, LightGBMConfig,
    RiskAssessmentModel, RiskAssessmentConfig,
    VulnerabilityPredictor, VulnerabilityPredictorConfig,
    ExplainabilityChain, ExplainabilityConfig,
    GNNVulnerabilityPredictor, GNNVulnerabilityPredictorConfig,
    DependencyGraphBuilder, DependencyGraphConfig,
    DependencyGraphAnalyzer, DependencyGraphAnalyzerConfig
)

from .utils.monitoring import track_request_duration, record_model_metrics
from .utils.cache import Cache
from .config import get_config
from .protos import sbomai_ai_pb2 as pb2
from .protos import sbomai_ai_pb2_grpc as pb2_grpc

logger = logging.getLogger(__name__)

class SbomaiAiService(pb2_grpc.SbomaiAiServiceServicer):
    """
    SBOMAI AI service implementation.
    """
    
    def __init__(self):
        self.config = get_config()
        self.cache = Cache()
        
        # Initialize models
        self.openai_model = OpenAiModel(OpenAiConfig(
            api_key=self.config.openai_api_key,
            model=self.config.openai_model
        ))
        
        self.anthropic_model = AnthropicModel(AnthropicConfig(
            api_key=self.config.anthropic_api_key,
            model=self.config.anthropic_model
        ))
        
        self.google_model = GoogleGeminiModel(GoogleGeminiConfig(
            api_key=self.config.google_api_key,
            model=self.config.google_model
        ))
        
        self.local_model = LocalTransformerModel(LocalTransformerConfig())
        
        self.xgboost_model = XGBoostRiskModel(XGBoostConfig())
        self.lightgbm_model = LightGBMRiskModel(LightGBMConfig())
        
        self.risk_model = RiskAssessmentModel(RiskAssessmentConfig(
            xgboost_config=XGBoostConfig(),
            lightgbm_config=LightGBMConfig()
        ))
        
        self.predictor = VulnerabilityPredictor(VulnerabilityPredictorConfig())
        
        self.explainability = ExplainabilityChain(ExplainabilityConfig(
            llm_type=self.config.default_llm,
            api_key=getattr(self.config, f"{self.config.default_llm}_api_key"),
            model_name=getattr(self.config, f"{self.config.default_llm}_model")
        ))
        
        self.gnn_predictor = GNNVulnerabilityPredictor(
            GNNVulnerabilityPredictorConfig()
        )
        
        self.graph_builder = DependencyGraphBuilder(DependencyGraphConfig())
        
        self.graph_analyzer = DependencyGraphAnalyzer(
            DependencyGraphAnalyzerConfig(
                graph_builder_config=DependencyGraphConfig()
            )
        )
    
    @track_request_duration
    async def AnalyzeSbom(
        self,
        request: pb2.AnalyzeSbomRequest,
        context: grpc.aio.ServicerContext
    ) -> pb2.AnalyzeSbomResponse:
        """
        Analyze SBOM document.
        """
        try:
            # Check cache
            cache_key = f"sbom:{hash(request.sbom_data)}"
            cached = await self.cache.get(cache_key)
            if cached:
                return pb2.AnalyzeSbomResponse(**cached)
            
            # Parse SBOM data
            sbom_data = self._parse_sbom(request.sbom_data)
            
            # Build and analyze dependency graph
            graph = self.graph_builder.build_graph(sbom_data)
            graph_analysis = self.graph_analyzer.analyze_dependencies(sbom_data)
            
            # Get risk assessment
            risk_analysis = await self.risk_model.analyze_vulnerability({
                'components': sbom_data.get('components', []),
                'vulnerabilities': sbom_data.get('vulnerabilities', [])
            })
            
            # Get predictions
            predictions = await self.predictor.analyze_vulnerability({
                'components': sbom_data.get('components', []),
                'vulnerabilities': sbom_data.get('vulnerabilities', [])
            })
            
            # Get GNN predictions
            gnn_predictions = await self.gnn_predictor.analyze_vulnerability({
                'components': sbom_data.get('components', []),
                'vulnerabilities': sbom_data.get('vulnerabilities', [])
            })
            
            # Get explainability analysis
            explanations = await self.explainability.analyze_vulnerability({
                'components': sbom_data.get('components', []),
                'vulnerabilities': sbom_data.get('vulnerabilities', [])
            })
            
            # Combine results
            response = pb2.AnalyzeSbomResponse(
                graph_analysis=self._convert_graph_analysis(graph_analysis),
                risk_analysis=self._convert_risk_analysis(risk_analysis),
                predictions=self._convert_predictions(predictions),
                gnn_predictions=self._convert_gnn_predictions(gnn_predictions),
                explanations=self._convert_explanations(explanations)
            )
            
            # Cache results
            await self.cache.set(
                cache_key,
                response.SerializeToString(),
                ttl=self.config.cache_ttl
            )
            
            # Record metrics
            self._record_metrics(response)
            
            return response
        
        except Exception as e:
            logger.error(f"Error analyzing SBOM: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return pb2.AnalyzeSbomResponse()
    
    @track_request_duration
    async def StreamAnalysis(
        self,
        request: pb2.StreamAnalysisRequest,
        context: grpc.aio.ServicerContext
    ) -> AsyncGenerator[pb2.StreamAnalysisResponse, None]:
        """
        Stream analysis results.
        """
        try:
            # Parse SBOM data
            sbom_data = self._parse_sbom(request.sbom_data)
            
            # Stream graph analysis
            graph = self.graph_builder.build_graph(sbom_data)
            graph_analysis = self.graph_analyzer.analyze_dependencies(sbom_data)
            
            yield pb2.StreamAnalysisResponse(
                type='graph',
                data=self._convert_graph_analysis(graph_analysis)
            )
            
            # Stream risk analysis
            risk_analysis = await self.risk_model.analyze_vulnerability({
                'components': sbom_data.get('components', []),
                'vulnerabilities': sbom_data.get('vulnerabilities', [])
            })
            
            yield pb2.StreamAnalysisResponse(
                type='risk',
                data=self._convert_risk_analysis(risk_analysis)
            )
            
            # Stream predictions
            predictions = await self.predictor.analyze_vulnerability({
                'components': sbom_data.get('components', []),
                'vulnerabilities': sbom_data.get('vulnerabilities', [])
            })
            
            yield pb2.StreamAnalysisResponse(
                type='predictions',
                data=self._convert_predictions(predictions)
            )
            
            # Stream GNN predictions
            gnn_predictions = await self.gnn_predictor.analyze_vulnerability({
                'components': sbom_data.get('components', []),
                'vulnerabilities': sbom_data.get('vulnerabilities', [])
            })
            
            yield pb2.StreamAnalysisResponse(
                type='gnn',
                data=self._convert_gnn_predictions(gnn_predictions)
            )
            
            # Stream explanations
            explanations = await self.explainability.analyze_vulnerability({
                'components': sbom_data.get('components', []),
                'vulnerabilities': sbom_data.get('vulnerabilities', [])
            })
            
            yield pb2.StreamAnalysisResponse(
                type='explanations',
                data=self._convert_explanations(explanations)
            )
        
        except Exception as e:
            logger.error(f"Error streaming analysis: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            yield pb2.StreamAnalysisResponse()
    
    def _parse_sbom(self, sbom_data: str) -> Dict:
        """Parse SBOM data"""
        # TODO: Implement SBOM format detection and parsing
        return {}
    
    def _convert_graph_analysis(self, analysis: Dict) -> pb2.GraphAnalysis:
        """Convert graph analysis to protobuf"""
        return pb2.GraphAnalysis()  # TODO: Implement conversion
    
    def _convert_risk_analysis(self, analysis: Dict) -> pb2.RiskAnalysis:
        """Convert risk analysis to protobuf"""
        return pb2.RiskAnalysis()  # TODO: Implement conversion
    
    def _convert_predictions(self, predictions: Dict) -> pb2.Predictions:
        """Convert predictions to protobuf"""
        return pb2.Predictions()  # TODO: Implement conversion
    
    def _convert_gnn_predictions(self, predictions: Dict) -> pb2.GnnPredictions:
        """Convert GNN predictions to protobuf"""
        return pb2.GnnPredictions()  # TODO: Implement conversion
    
    def _convert_explanations(self, explanations: Dict) -> pb2.Explanations:
        """Convert explanations to protobuf"""
        return pb2.Explanations()  # TODO: Implement conversion
    
    def _record_metrics(self, response: pb2.AnalyzeSbomResponse):
        """Record response metrics"""
        record_model_metrics(
            'graph_analysis',
            len(response.graph_analysis.SerializeToString())
        )
        record_model_metrics(
            'risk_analysis',
            len(response.risk_analysis.SerializeToString())
        )
        record_model_metrics(
            'predictions',
            len(response.predictions.SerializeToString())
        )
        record_model_metrics(
            'gnn_predictions',
            len(response.gnn_predictions.SerializeToString())
        )
        record_model_metrics(
            'explanations',
            len(response.explanations.SerializeToString())
        )

async def serve():
    """Start gRPC server"""
    server = grpc.aio.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[
            ('grpc.max_send_message_length', 50 * 1024 * 1024),
            ('grpc.max_receive_message_length', 50 * 1024 * 1024)
        ]
    )
    
    pb2_grpc.add_SbomaiAiServiceServicer_to_server(
        SbomaiAiService(),
        server
    )
    
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    
    logger.info(f"Starting server on {listen_addr}")
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())