"""
This file contains actions for reader agent.
"""
import asyncio
import json
from typing import ClassVar
from base.core.action import Action
from base.core.logs import logger
from base.core.schema import Message
from core.model.read_report import ReadReport, SingleFuncReport
from core.model.vuln_report import VulnReport
from core.utils.service import LLMService

class ReadCode(Action):
    """
    This class is an action for reader agent.
    """
    PROMPT_TEMPLATE:ClassVar[str]="""
    You are tasked with analyzing function(s) mentioned in vulnerability report(s). Review the provided code and vulnerability reports to generate a structured analysis following these requirements:

    ANALYSIS REQUIREMENTS:
    1. Identify ALL functions referenced in vulnerability reports' sink points
    2. For each identified function:
    - Determine its primary purpose
    - Analyze implementation details
    - Document key execution steps
    3. Include ALL functions mentioned, no exceptions
    4. Focus specifically on sink points from vulnerability reports

    OUTPUT REQUIREMENTS:
    1. Return ONLY a valid JSON array without any additional text or code fences.
    2. Each function analysis must be a separate object in the array. Only include fields from the base model below.
    3. NO additional text/comments outside JSON structure
    4. NO markdown formatting or code fences
    5. Strict adherence to the following schema:

    {expected_schema}

    VALIDATION RULES:
    1. functionName must exactly match sink point reference
    2. functionPurpose must be clear and concise
    3. functionImplementation must contain ordered, logical steps
    4. All strings must be properly escaped
    5. JSON must be parseable

    INPUT CONTEXT:
    Code to analyze:
    {code_text}

    Vulnerability report(s):
    {report_text}

    Your analysis in JSON format without code fences and adhere the schema:

    """
    name:str="ReadCode"
    desc:str="This action is used to read the code."
    async def run(self,code_text:str,reports:VulnReport)->ReadReport:
        service=LLMService() # Initialize the singleton service
        prompt = self.PROMPT_TEMPLATE.format(code_text=code_text,report_text=reports.model_dump_json(),expected_schema=ReadReport.model_json_schema()) # NOTE: Dump the reports to json string
        res=await service.generate_structured_async(prompt,ReadReport)
        
        if not isinstance(res, ReadReport):
            logger.info(f"ReadCode response: {res.model_dump_json()}")
            raise ValueError(f"Invalid response from ReadCode. Stop execution: {type(res)},{res.model_dump_json()}")
        return res
    