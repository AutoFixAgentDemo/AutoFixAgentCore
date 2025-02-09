from typing import ClassVar
from base.core.action import Action
from base.core.logs import logger
from base.core.schema import Message
from core.model.repair import OverallRepair
from core.model.read_report import ReadReport
from core.model.vuln_report import VulnReport
from core.model.verify import OverallVerify
from core.utils.service import LLMService
class GeneralVerify(Action):
    PROMPT_TEMPLATE:ClassVar[str]="""
    You are a security and code quality verifier. Your task is to review the provided materials to determine if the vulnerability fixes have been applied correctly without interfering with the original functionality of the code.

    You will be given the following inputs:
    1. The complete source code text.
    2. A reading comprehension report of the related functions.
    3. A vulnerability report detailing one or more vulnerabilities.
    4. A diff file representing the patch intended to fix the vulnerabilities.

    For each vulnerability described in the vulnerability report, please:
    1. Determine whether the provided patch (as per the diff file) fixes the vulnerability without altering the original program functionality.
    2. Provide a clear and human-readable explanation that supports your verification decision.

    Your final output must strictly be in JSON format and conform exactly to the following data model:

    - For each vulnerability, output an object with two keys:
      - "verify_status": A boolean value indicating whether the fix was applied correctly (true if fixed without affecting functionality, false otherwise).
      - "verify_message": A detailed explanation of your verification process and conclusion.

    - The overall JSON object must follow this structure:
      
      {expected_schema}

    Ensure that:
    - There is no extraneous text or additional keys in your output.
    - Your answer is strictly valid JSON and no commentary or explanations outside the JSON structure are provided.

    Inputs provided:
    1. **Code File**:
    ```
    {code_text}
    ```
    2. **Code Understanding Report**:
    {read_reports}

    3. **Vulnerability Detection Report**:
    {vuln_reports}

    4. **Patch Diff**:
    {diff_texts}

    Begin your analysis with the provided input and then output the verification results accordingly.Your Response (ONLY JSON):
    """
    name:str="GeneralVerify"
    desc:str="This action verifies the correctness of the applied patches."
    async def run(self,code_text:str,vuln_reports:VulnReport,read_reports:ReadReport,diff_texts:OverallRepair)->OverallVerify:
        service=LLMService() # Initialize the singleton service
        prompt=self.PROMPT_TEMPLATE.format(code_text=code_text,vuln_reports=vuln_reports.model_dump(),read_reports=read_reports.model_dump(),diff_texts=diff_texts.model_dump(),expected_schema=OverallVerify.model_json_schema())
        res=await service.generate_structured_async(prompt,OverallVerify)
        return res