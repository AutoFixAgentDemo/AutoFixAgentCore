"""
This file defines a manager class to manage different LLM model types."""
from typing import Dict, Any
import json
from .meta import BaseLLMClient, LLMMeta
from dynaconf import settings
from pydantic import BaseModel
from base.core.logs import logger
class LLMManager:
    def __init__(self, config: Dict[str, Any] = None, **kwargs):
        self.config = config or kwargs
        self.client = self._init_client()
        logger.info(f"Initialized LLM manager with config: {self.config}")
    
    def _init_client(self) -> BaseLLMClient:
        config = self.config.copy()
        client_type = config.pop('type')
        client_class = LLMMeta.get_client(client_type)
        return client_class(**config)
    
    def generate_plain(self, prompt: str) -> str:
        return self.client.generate_plain(prompt)
    def generate_structured(self, prompt: str,excepted_model:BaseModel) -> BaseModel:
        return self.client.generate_structured(prompt,excepted_model)