"""
The implementations of the Ollama provider."""

from .base.meta import BaseLLMClient
from pydantic import BaseModel
from urllib.parse import urljoin
from .util import send_request
import instructor
from openai import OpenAI
from dynaconf import settings

class OllamaClient(BaseLLMClient):
    def __init__(self,host:str,model:str,api_key:str):
        """
        Initialize the Ollama client.
        Args:
            host: The base URL of the Ollama API. Should be like "https://localhost:8000".
            model: The model name.
        """
        self.host = host
        self.model_name = model
        self.api_key = api_key
        self._setup()
        
    def _setup(self):
        """
        Setup a client complatible with the Ollama API using OpenAI for instructor.
        """
        self.client = instructor.from_openai(
        OpenAI(
            base_url=urljoin(self.host, "/v1"),
            api_key=self.api_key,
        ),mode=instructor.Mode.JSON,)
    def generate_plain(self, prompt: str) -> str:
        """
        Generate a completion without structured data.
        Args:
            prompt: The prompt text.
        Returns:
            The generated completion.
        """
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
        }
        
        # Use urljoin to build the URL
        url= urljoin(self.host, "/api/generate")
        # NOTE: base url should only be the domain like "https://localhost:8000"

        # Retry the request for 3 times
        try:
            resp=send_request(url,data)
        except Exception as e:
            raise RuntimeError(f"Failed to request: {str(e)}")
        return resp
    def generate_structured(self, prompt: str,expected_model:BaseModel) -> BaseModel:
        """
        Generate a completion with structured data using instructor via /chat/.
        Args:
            prompt: The prompt text.
            excepted_model: The expected model to validate.
        """
        resp=self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            response_model=expected_model,
            max_retries=settings.get("core.max_retries", default=3),
        )
        return resp
    @DeprecationWarning
    def generate_structured_legacy(self, prompt: str,expected_model:BaseModel) -> BaseModel:
        """
        Generate a completion with structured data which fits the givel model. Deprecated for 400 bug.
        Args:
            prompt: The prompt text.
            excepted_model: The expected model to validate.
        Returns:
            The generated completion.
        """
        # 从Pydantic模型生成JSON Schema
        schema = expected_model.model_json_schema()
        
        # Build the format spec
        format_spec = {
            "type": "object",
            "properties": schema["properties"],
            "required": schema.get("required", [])
        }
        
        # prepare the data
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "format": str(schema)
        }
        
        # Use urljoin to build the URL
        url= urljoin(self.host, "/api/generate")
        # NOTE: base url should only be the domain like "https://localhost:8000"

        # Retry the request for 3 times
        try:
            resp=send_request(url,data,expected_model)
        except Exception as e:
            raise RuntimeError(f"Failed to request: {str(e)}")
        
        return resp
        