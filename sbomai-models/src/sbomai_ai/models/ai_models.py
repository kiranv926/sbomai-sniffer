"""
AI model implementations for SBOM analysis
"""

import asyncio
import time
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
import logging

import openai
import anthropic
import google.generativeai as genai
from transformers import pipeline, AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
import torch

from ..config import get_config
from ..utils.exceptions import AiModelError

logger = logging.getLogger(__name__)


class BaseAiModel(ABC):
    """Base class for AI models"""
    
    def __init__(self, model_name: str, provider: str):
        self.model_name = model_name
        self.provider = provider
        self.config = get_config()
        self.is_available = False
        
    @abstractmethod
    async def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate response from the AI model"""
        pass
    
    @abstractmethod
    def is_model_available(self) -> bool:
        """Check if the model is available"""
        pass
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            "name": self.model_name,
            "provider": self.provider,
            "available": self.is_available,
        }


class OpenAiModel(BaseAiModel):
    """OpenAI GPT model implementation"""
    
    def __init__(self):
        super().__init__(
            model_name=self.config.ai_provider.openai_model,
            provider="openai"
        )
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize OpenAI client"""
        if self.config.ai_provider.openai_api_key:
            try:
                self.client = openai.AsyncOpenAI(
                    api_key=self.config.ai_provider.openai_api_key,
                    timeout=self.config.ai_provider.openai_timeout
                )
                self.is_available = True
                logger.info("OpenAI client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
                self.is_available = False
        else:
            logger.warning("OpenAI API key not provided")
            self.is_available = False
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate response using OpenAI GPT"""
        if not self.is_available:
            raise AiModelError("OpenAI model is not available")
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=kwargs.get("max_tokens", self.config.ai_provider.openai_max_tokens),
                temperature=kwargs.get("temperature", self.config.ai_provider.openai_temperature),
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise AiModelError(f"OpenAI API error: {e}")
    
    def is_model_available(self) -> bool:
        return self.is_available
    
    def _get_system_prompt(self) -> str:
        return """You are an expert cybersecurity analyst specializing in Software Bill of Materials (SBOM) analysis. 
        Your role is to assess security risks in software components and provide actionable recommendations. 
        Always provide structured, professional analysis with clear risk levels and specific recommendations. 
        Focus on identifying potential vulnerabilities, outdated components, and security best practices."""


class AnthropicModel(BaseAiModel):
    """Anthropic Claude model implementation"""
    
    def __init__(self):
        super().__init__(
            model_name=self.config.ai_provider.anthropic_model,
            provider="anthropic"
        )
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Anthropic client"""
        if self.config.ai_provider.anthropic_api_key:
            try:
                self.client = anthropic.AsyncAnthropic(
                    api_key=self.config.ai_provider.anthropic_api_key
                )
                self.is_available = True
                logger.info("Anthropic client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Anthropic client: {e}")
                self.is_available = False
        else:
            logger.warning("Anthropic API key not provided")
            self.is_available = False
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate response using Anthropic Claude"""
        if not self.is_available:
            raise AiModelError("Anthropic model is not available")
        
        try:
            response = await self.client.messages.create(
                model=self.model_name,
                max_tokens=kwargs.get("max_tokens", self.config.ai_provider.anthropic_max_tokens),
                temperature=kwargs.get("temperature", self.config.ai_provider.anthropic_temperature),
                messages=[
                    {"role": "user", "content": f"{self._get_system_prompt()}\n\n{prompt}"}
                ],
                **kwargs
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise AiModelError(f"Anthropic API error: {e}")
    
    def is_model_available(self) -> bool:
        return self.is_available
    
    def _get_system_prompt(self) -> str:
        return """You are an expert cybersecurity analyst specializing in Software Bill of Materials (SBOM) analysis. 
        Your role is to assess security risks in software components and provide actionable recommendations. 
        Always provide structured, professional analysis with clear risk levels and specific recommendations. 
        Focus on identifying potential vulnerabilities, outdated components, and security best practices."""


class GoogleGeminiModel(BaseAiModel):
    """Google Gemini model implementation"""
    
    def __init__(self):
        super().__init__(
            model_name=self.config.ai_provider.google_model,
            provider="google"
        )
        self.model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize Google Gemini model"""
        if self.config.ai_provider.google_api_key:
            try:
                genai.configure(api_key=self.config.ai_provider.google_api_key)
                self.model = genai.GenerativeModel(self.model_name)
                self.is_available = True
                logger.info("Google Gemini model initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Google Gemini model: {e}")
                self.is_available = False
        else:
            logger.warning("Google API key not provided")
            self.is_available = False
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate response using Google Gemini"""
        if not self.is_available:
            raise AiModelError("Google Gemini model is not available")
        
        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                f"{self._get_system_prompt()}\n\n{prompt}",
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=kwargs.get("max_tokens", self.config.ai_provider.google_max_tokens),
                    temperature=kwargs.get("temperature", self.config.ai_provider.google_temperature),
                )
            )
            return response.text
        except Exception as e:
            logger.error(f"Google Gemini API error: {e}")
            raise AiModelError(f"Google Gemini API error: {e}")
    
    def is_model_available(self) -> bool:
        return self.is_available
    
    def _get_system_prompt(self) -> str:
        return """You are an expert cybersecurity analyst specializing in Software Bill of Materials (SBOM) analysis. 
        Your role is to assess security risks in software components and provide actionable recommendations. 
        Always provide structured, professional analysis with clear risk levels and specific recommendations. 
        Focus on identifying potential vulnerabilities, outdated components, and security best practices."""


class LocalTransformerModel(BaseAiModel):
    """Local transformer model implementation using HuggingFace"""
    
    def __init__(self, model_path: Optional[str] = None):
        model_path = model_path or self.config.ai_provider.local_model_path
        super().__init__(
            model_name=model_path or "sentence-transformers/all-MiniLM-L6-v2",
            provider="local"
        )
        self.tokenizer = None
        self.model = None
        self.device = self.config.ai_provider.local_device
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize local transformer model"""
        try:
            if self.config.ai_provider.local_model_type == "sentence-transformers":
                self.model = SentenceTransformer(self.model_name, device=self.device)
                self.is_available = True
                logger.info(f"Local transformer model initialized: {self.model_name}")
            else:
                # For other transformer types (text generation, etc.)
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModel.from_pretrained(self.model_name)
                if torch.cuda.is_available() and self.device == "cuda":
                    self.model = self.model.cuda()
                self.is_available = True
                logger.info(f"Local transformer model initialized: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize local transformer model: {e}")
            self.is_available = False
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate response using local transformer model"""
        if not self.is_available:
            raise AiModelError("Local transformer model is not available")
        
        try:
            # For sentence transformers, we'll use similarity-based response generation
            if isinstance(self.model, SentenceTransformer):
                return await self._generate_similarity_response(prompt, **kwargs)
            else:
                return await self._generate_text_response(prompt, **kwargs)
        except Exception as e:
            logger.error(f"Local transformer model error: {e}")
            raise AiModelError(f"Local transformer model error: {e}")
    
    async def _generate_similarity_response(self, prompt: str, **kwargs) -> str:
        """Generate response using similarity-based approach"""
        # This is a simplified implementation - in practice, you'd have a knowledge base
        # of SBOM analysis responses and find the most similar one
        embeddings = await asyncio.to_thread(self.model.encode, prompt)
        
        # For now, return a template response based on keywords
        if "vulnerability" in prompt.lower():
            return "Based on the analysis, this component shows potential security vulnerabilities. Consider upgrading to a newer version or implementing additional security measures."
        elif "outdated" in prompt.lower():
            return "This component appears to be outdated. Updating to the latest stable version is recommended to address potential security and compatibility issues."
        else:
            return "The component analysis indicates moderate risk. Regular monitoring and updates are recommended."
    
    async def _generate_text_response(self, prompt: str, **kwargs) -> str:
        """Generate text response using the transformer model"""
        inputs = await asyncio.to_thread(
            self.tokenizer.encode,
            prompt,
            return_tensors="pt",
            max_length=512,
            truncation=True
        )
        
        if torch.cuda.is_available() and self.device == "cuda":
            inputs = inputs.cuda()
        
        with torch.no_grad():
            outputs = await asyncio.to_thread(self.model.generate, inputs, **kwargs)
        
        response = await asyncio.to_thread(
            self.tokenizer.decode,
            outputs[0],
            skip_special_tokens=True
        )
        
        return response
    
    def is_model_available(self) -> bool:
        return self.is_available
    
    def get_embeddings(self, text: str) -> List[float]:
        """Get embeddings for text"""
        if not self.is_available:
            raise AiModelError("Local transformer model is not available")
        
        if isinstance(self.model, SentenceTransformer):
            return self.model.encode(text).tolist()
        else:
            raise AiModelError("Embeddings not supported for this model type")


class AiModelFactory:
    """Factory for creating AI models"""
    
    @staticmethod
    def create_model(provider: str) -> BaseAiModel:
        """Create AI model based on provider"""
        if provider == "openai":
            return OpenAiModel()
        elif provider == "anthropic":
            return AnthropicModel()
        elif provider == "google":
            return GoogleGeminiModel()
        elif provider == "local":
            return LocalTransformerModel()
        else:
            raise ValueError(f"Unsupported AI provider: {provider}")
    
    @staticmethod
    def get_available_models() -> List[BaseAiModel]:
        """Get list of available AI models"""
        config = get_config()
        available_models = []
        
        providers = ["openai", "anthropic", "google", "local"]
        for provider in providers:
            try:
                model = AiModelFactory.create_model(provider)
                if model.is_model_available():
                    available_models.append(model)
            except Exception as e:
                logger.warning(f"Failed to create model for provider {provider}: {e}")
        
        return available_models
    
    @staticmethod
    def get_best_available_model() -> Optional[BaseAiModel]:
        """Get the best available AI model based on priority"""
        available_models = AiModelFactory.get_available_models()
        
        if not available_models:
            return None
        
        # Priority order: OpenAI > Anthropic > Google > Local
        priority_order = ["openai", "anthropic", "google", "local"]
        
        for provider in priority_order:
            for model in available_models:
                if model.provider == provider:
                    return model
        
        return available_models[0]  # Fallback to first available 