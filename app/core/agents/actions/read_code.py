"""
This file contains actions for reader agent.
"""
import asyncio
import json
from typing import ClassVar
from base.core.action import Action
from base.core.logs import logger
from base.core.schema import Message
from model.read_report import ReadReport, SingleFuncReport
from model.vuln_report import VulnReport
class ReadCode(Action):
    """
    This class is an action for reader agent.
    """
    PROMPT_TEMPLATE:ClassVar[str]="""
    You have been provided with a vulnerabilities report list which may contains multiple vulnerbility reports. Within this report, there is a mention of a particular function. Your task is to analyze that function and provide a concise report. Please follow these steps:
        1.	Identify the functions referenced in the vulnerability report.
        2.	Determine the purpose of the each function. Explain what the function is supposed to do.
        3.	Understand the implementation details of the function. Summarize how it is or should be implemented.
        4.	Write your findings in a final report, following the format instructions below and never ignore any functions mentioned in the report's sink point.

    Important:
        1. Your final output must be returned as valid JSON only. No code fence needed.
        2. Do not include any additional text, markdown, or formatting outside of the JSON structure.

    Use the following JSON format for your final answer as a list of a dictionary with the following fixed code:

    [{{
    "functionName": "Name of the function or the method which contains the sink point mentioned in the report",
    "functionPurpose": "Short explanation of the function's purpose",
    "functionImplementation": ["A list of key steps on how the function is or should be implemented"]
    }}]
    Return only the JSON object—no extra commentary, headers, or descriptive text.

    Below is the code snippet you need to analyze:

    {code_text}

    Below is the vulnerability report may contain multiple vulns:

    {report_text}

    Your answer:

    """
    name:str="ReadCode"
    desc:str="This action is used to read the code."
    async def run(self,code_text:str,reports:VulnReport)->ReadReport:

        prompt = self.PROMPT_TEMPLATE.format(code_text=code_text,report_text=reports.model_dump_json()) # NOTE: Dump the reports to json string
        
        max_attempts = 3
        for attempt in range(max_attempts):
            rsp = await self._aask(prompt)
            try:
                json.loads(rsp)
                res=ReadReport(**json.loads(rsp))
                break
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON response from ReadCode. Attempt {attempt+1}/{max_attempts}")
                if attempt == max_attempts - 1:
                    # TODO: Add error handling here
                    raise ValueError("Invalid JSON response from ReadCode. Maximum attempts reached.")
                return 
            except Exception as e:
                logger.error(f"Error in parsing the JSON response from ReadCode: {e}")
                if attempt == max_attempts - 1:
                    raise ValueError(f"Error in parsing the JSON response from ReadCode: {e}")
                return
            
        return res
    