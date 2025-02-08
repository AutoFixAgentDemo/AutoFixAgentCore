from base.core.action import Action
from config import settings # Import the settings from the config.py file instead of the Dynaconf library but why? Dont change it.
from pydantic import BaseModel
from base.core.logs import logger
import asyncio
import json
from typing import Dict, Any
from .provider.base.manager import LLMManager
from .provider.base.meta import LLMMeta

class LLMService:
    """
    This class is used to communicate with the remote LLM API. It is herited from the BaseLLM class in provider."""
    def __init__(
        self,
        **kwargs
    ):
        """
        Initialize the LLM service.
        Args:
            llm_type: The LLM type.
            **kwargs: The configuration parameters to initialize LLM bypass the settings.toml(Not recommended).
        """
        
        if kwargs:
            self.config = kwargs # NOTE: Not recommended but can override the settings.toml using explicit parameters.
        else:
            print(settings.get('llm'))
            self.config = settings.get("llm", default={})
        
        logger.info(f"Initialized LLM service with config: {self.config}")
        if not self.config:
            raise ValueError("No LLM configuration found.")
        for key in ["type", "model", "host", "api_key"]:
            if key not in self.config:
                if key == "api_key": # NOTE: Some LLMs may not require an API key.
                    self.config[key] = "N/A"
                else:
                    raise ValueError(f"Missing LLM configuration key: {key}")
        
        """
        NOTE: A complete config should be like:
        In settings.toml:
        [llm]
        type="Ollama"
        model="qwen2.5:32b" 
        In .secret.toml:
        [llm]
        host="http://172.17.0.16:11434"
        api_key="your_api_key"(Optional but cannot be empty for instructor lib)
        """

        self.manager = LLMManager(**self.config)

    @staticmethod
    def list_available_llms() -> list:
        """列出所有可用的LLM类型"""
        return list(LLMMeta.list_clients().keys())
    
    def generate_plain(self, prompt: str) -> str:
        """
        Generate a completion without structured data.
        Args:
            prompt: The prompt text.
        Returns:
            The generated completion.
        """
        try:
            return self.manager.generate_plain(prompt)
        except Exception as e:
            raise ValueError(f"Failed to generate plain completion: {str(e)}")
        
    def generate_structured(self, prompt: str,excepted_model:BaseModel) -> BaseModel:
        """
        Generate a completion with structured data which fits the givel model.
        Args:
            prompt: The prompt text.
            excepted_model: The expected model to validate.
        Returns:
            The generated completion.
        """
        try:
            return self.manager.generate_structured(prompt,excepted_model)
        except Exception as e:
            raise ValueError(f"Failed to generate structured completion: {str(e)}")
    
    @DeprecationWarning
    async def ask_structured_resp(cls:Action,prompt:str,excepted_resp_model:BaseModel)->BaseModel:
        """
        This method is used to wrap the ask process to communicate with remote LLM API.
        We add some validations and error handling to retry the ask process if it fails.

        :param cls: Action class object which calls this method.
        :type cls: Action
        :param prompt: The filled prompt message to be sent to the LLM API.
        :type prompt: str
        :param excepted_resp_model: The expected response model to validate the response.
        :type excepted_resp_model: BaseModel

        :return: The validated response model object. None if the response is invalid.
        """
        max_attempts = settings.get("core.max_retries", default=3)
        for attempt in range(max_attempts):
            rsp = await cls._aask(prompt)
            logger.debug(f"Response from {cls.name} with attempts {attempt} : {rsp}")
            try:
                json.loads(rsp)
                res=excepted_resp_model(**json.loads(rsp))
                break
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON response from {cls.name}. Attempt {attempt+1}/{max_attempts}")
                if attempt == max_attempts - 1:
                    # TODO: Add error handling here
                    raise ValueError(f"Invalid JSON response from {cls.name}. Maximum attempts reached.")
                     
            except Exception as e:
                logger.error(f"Error in parsing the JSON response from {cls.name}: {e}")
                if attempt == max_attempts - 1:
                    raise ValueError(f"Error in parsing the JSON response from {cls.name}: {e}. Maximum attempts reached.")
                
        return res
