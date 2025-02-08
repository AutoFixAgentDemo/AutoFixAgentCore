from typing import Type, TypeVar,Union
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from dynaconf import settings
from pydantic import BaseModel
@retry(stop=stop_after_attempt(settings.get("core.max_retries", default=3)), wait=wait_exponential(multiplier=1, min=4, max=10))
def send_request(url:str,data:dict,expected_model:BaseModel=None)-> Union[BaseModel, str]:
    print(f"Sending request to {url} with data: {data}")
    try:
        headers = {
            "Content-Type": "application/json"
        }
        with httpx.Client(timeout=httpx.Timeout(settings.get("request.timeout",default=60))) as client:
            response = client.post(url,headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            
        # Extract the generated JSON
        resp = result["response"]
        if expected_model:
            # Validate the generated JSON
            parsed_model = expected_model.model_validate(resp)
            return parsed_model
        else:
            #Plain mode
            return resp
            
    except httpx.HTTPError as e:
        raise RuntimeError(f"Failed to request: {str(e)}")
    except ValueError as e:
        raise ValueError(f"Failed to validate model: {str(e)}")