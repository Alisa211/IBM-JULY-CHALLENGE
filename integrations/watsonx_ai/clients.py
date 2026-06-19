"""
Watsonx.ai Client

This module handles all communication with IBM Watsonx.ai API.
Responsible for authentication, sending requests, and receiving responses.
"""

import logging
from typing import Optional, Dict, Any
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai import Credentials

logger = logging.getLogger(__name__)


class WatsonxClient:
    """
    Client for interacting with IBM Watsonx.ai Foundation Models.
    
    This client handles:
    - Authentication with IBM Cloud
    - Model initialization
    - Prompt submission
    - Response retrieval
    """
    
    def __init__(
        self,
        api_key: str,
        project_id: str,
        url: str = "https://us-south.ml.cloud.ibm.com",
        model_id: str = "ibm/granite-13b-instruct-v2"
    ):
        """
        Initialize Watsonx client.
        
        Args:
            api_key: IBM Cloud API key
            project_id: Watsonx project ID
            url: Watsonx API endpoint URL
            model_id: Model identifier to use
        """
        self.api_key = api_key
        self.project_id = project_id
        self.url = url
        self.model_id = model_id
        self._model: Optional[ModelInference] = None
        
        logger.info(f"Initializing WatsonxClient with model: {model_id}")
    
    def _get_credentials(self) -> Credentials:
        """
        Create credentials object for authentication.
        
        Returns:
            Credentials object
        """
        return Credentials(
            api_key=self.api_key,
            url=self.url
        )
    
    def _initialize_model(self) -> ModelInference:
        """
        Initialize the foundation model.
        
        Returns:
            ModelInference instance
        """
        if self._model is None:
            credentials = self._get_credentials()
            
            self._model = ModelInference(
                model_id=self.model_id,
                credentials=credentials,
                project_id=self.project_id
            )
            
            logger.info("Model initialized successfully")
        
        return self._model
    
    def generate(
        self,
        prompt: str,
        max_new_tokens: int = 1000,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 50,
        repetition_penalty: float = 1.1,
        **kwargs
    ) -> str:
        """
        Generate text using the foundation model.
        
        Args:
            prompt: Input prompt text
            max_new_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0-2.0)
            top_p: Nucleus sampling parameter
            top_k: Top-k sampling parameter
            repetition_penalty: Penalty for repetition
            **kwargs: Additional model parameters
            
        Returns:
            Generated text response
            
        Raises:
            Exception: If generation fails
        """
        try:
            model = self._initialize_model()
            
            # Prepare generation parameters
            params = {
                "max_new_tokens": max_new_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "repetition_penalty": repetition_penalty,
                **kwargs
            }
            
            logger.info(f"Generating with params: {params}")
            logger.debug(f"Prompt length: {len(prompt)} characters")
            
            # Generate response
            response = model.generate_text(
                prompt=prompt,
                params=params
            )
            
            logger.info(f"Generation successful, response length: {len(str(response))} characters")
            
            # Ensure we return a string
            if isinstance(response, str):
                return response
            elif isinstance(response, dict):
                # If response is a dict, extract the generated text
                return str(response.get('generated_text', str(response)))
            elif isinstance(response, list):
                # If response is a list, join or take first element
                return str(response[0]) if response else ""
            else:
                return str(response)
            
        except Exception as e:
            logger.error(f"Generation failed: {str(e)}")
            raise Exception(f"Watsonx generation failed: {str(e)}")
    
    def generate_ideas(
        self,
        prompt: str,
        temperature: float = 0.8,
        max_new_tokens: int = 1500
    ) -> str:
        """
        Generate creative ideas with optimized parameters.
        
        Args:
            prompt: Input prompt for idea generation
            temperature: Higher temperature for more creativity
            max_new_tokens: Maximum tokens for detailed ideas
            
        Returns:
            Generated ideas text
        """
        return self.generate(
            prompt=prompt,
            temperature=temperature,
            max_new_tokens=max_new_tokens,
            top_p=0.95,
            repetition_penalty=1.2
        )
    
    def generate_critique(
        self,
        prompt: str,
        temperature: float = 0.5,
        max_new_tokens: int = 1000
    ) -> str:
        """
        Generate critique with balanced parameters.
        
        Args:
            prompt: Input prompt for critique
            temperature: Lower temperature for more focused analysis
            max_new_tokens: Maximum tokens for critique
            
        Returns:
            Generated critique text
        """
        return self.generate(
            prompt=prompt,
            temperature=temperature,
            max_new_tokens=max_new_tokens,
            top_p=0.9,
            repetition_penalty=1.1
        )
    
    def analyze_style(
        self,
        prompt: str,
        temperature: float = 0.6,
        max_new_tokens: int = 800
    ) -> str:
        """
        Analyze artistic style with optimized parameters.
        
        Args:
            prompt: Input prompt for style analysis
            temperature: Moderate temperature for balanced analysis
            max_new_tokens: Maximum tokens for analysis
            
        Returns:
            Generated style analysis text
        """
        return self.generate(
            prompt=prompt,
            temperature=temperature,
            max_new_tokens=max_new_tokens,
            top_p=0.9,
            repetition_penalty=1.15
        )
    
    def health_check(self) -> bool:
        """
        Check if the client can connect to Watsonx.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self._initialize_model()
            return True
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return False


# Singleton instance (will be initialized in service layer)
_client_instance: Optional[WatsonxClient] = None


def get_watsonx_client(
    api_key: str,
    project_id: str,
    url: str = "https://us-south.ml.cloud.ibm.com",
    model_id: str = "ibm/granite-13b-instruct-v2"
) -> WatsonxClient:
    """
    Get or create Watsonx client instance.
    
    Args:
        api_key: IBM Cloud API key
        project_id: Watsonx project ID
        url: Watsonx API endpoint URL
        model_id: Model identifier to use
        
    Returns:
        WatsonxClient instance
    """
    global _client_instance
    
    if _client_instance is None:
        _client_instance = WatsonxClient(
            api_key=api_key,
            project_id=project_id,
            url=url,
            model_id=model_id
        )
    
    return _client_instance

# Made with Bob
