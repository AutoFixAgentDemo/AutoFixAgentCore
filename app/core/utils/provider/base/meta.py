"""
This file defines an abstract class to fit different LLM model types.
"""
from abc import ABC, abstractmethod, ABCMeta
from typing import Dict,Any,Type
import json
from pydantic import BaseModel
from base.core.logs import logger
class LLMMeta(ABCMeta):
    _registry: Dict[str, Type['BaseLLMClient']] = {}
    
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if ABC not in bases and bases and issubclass(cls, BaseLLMClient):
            # generate registry name from class name
            registry_name = name.lower().replace('client', '')
            mcs._registry[registry_name] = cls
            logger.info(f"Registered LLM: {registry_name} -> {cls.__name__}")
        elif cls.__name__=='BaseLLMClient':
            return cls # NOTE: Skip the debug output for the base class
        else:
            logger.debug(f"Not registered the class {cls.__name__}(base class or ABC)")
        logger.debug(f"Current registry: {list(mcs._registry.keys())}")
        return cls
    
    @classmethod
    def get_client(mcs, name: str) -> Type['BaseLLMClient']:
        if name not in mcs._registry:
            raise ValueError(f"Unknown LLM type: {name}")
        return mcs._registry[name]
    
    @classmethod
    def list_clients(mcs) -> Dict[str, Type['BaseLLMClient']]:
        return mcs._registry.copy()


class BaseLLMClient(ABC,metaclass=LLMMeta):
    @abstractmethod
    def generate_plain(self, prompt: str) -> str:
        """
        To use generate endpoint to generate a completion without structured data."""
        pass
    
    @abstractmethod
    def generate_structured(self, prompt: str,expected_model:BaseModel) -> list:
        """
        To use generate endpoint to generate a completion with structured data which fits the givel model."""
        pass
    @abstractmethod
    async def generate_structured_async(self, prompt: str,expected_model:BaseModel) -> list:
        """
        To use generate endpoint to generate a completion with structured data asynchronously."""
        pass

