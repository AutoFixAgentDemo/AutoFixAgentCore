from base.core.action import Action
from dynaconf import settings
from pydantic import BaseModel
from base.core.logs import logger
import asyncio
import json
class Util:
    @staticmethod
    async def ask_wrap(cls:Action,prompt:str,excepted_resp_model:BaseModel)->BaseModel:
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
