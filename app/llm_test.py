"""
This is the file to test the reachbility of the LLM API.
"""


from core.utils.service import LLMService
from dynaconf import settings
from core.utils.provider.ollama import OllamaClient # NOTE: Import the OllamaClient class from the ollama.py file to register automatically.
from pydantic import BaseModel
class exampleModel(BaseModel):
    name:str
    score:float
if __name__=="__main__":
    
    print("Available LLMs:", LLMService.list_available_llms())

    # Initialize the configuration

    # Register by direct parameters to override settings.toml (Not recommended)
    service1 = LLMService(
        type="ollama",
        host="http://172.17.0.16:11434",
        api_key="N/A", # NOTE: You must put a value even if it is not required cause instructor lib need to do so.
        model="qwen2.5:32b"
    )
    print(f"service1 config: {service1.config}")
    # Register by settings.toml (recommended)
    
    service2 = LLMService()
    print(f"service2 config: {service2.config}")

    # Generate a completion
    #print(f"testing service1")
    #print(service1.generate_plain("Hello, world!"))
    #print(f"testing service2")
    #print(service2.generate_plain("Hello, world!"))

    # Generate a completion with structured data
    print(f"testing service2")
    res=service2.generate_structured(f"Tom got 90 points in the exam. Convert the fact to a json with the following format.Respond using JSON.",exampleModel)
    print(res,type(res))