import asyncio
import json
from typing import ClassVar
from base.core.action import Action
from base.core.logs import logger
from base.core.schema import Message
from core.model.repair import OverallRepair
from core.model.read_report import ReadReport
from core.model.vuln_report import VulnReport
from core.utils.service import LLMService
class GeneralRepair(Action):
    """
    This class is an action for repairer agent.
    """
    PROMPT_TEMPLATE:ClassVar[str]="""

    You are a security-focused code repair expert. Analyze the provided inputs and generate a minimal, effective patch for the each vulnerability while preserving original functionality. At last you need to output a single JSON object with two fields: `diff` and `report` to explain the patch solution for each vulnerbility. Leave evertything as it is and just apply the changes related to the fix.
    ### Inputs:  
    1. **Code File**:  
    ```  
    {code_file} 
    ``` 

    2. **Code Understanding Report**:  
    {read_report}

    3. **Vulnerability Detection Report**:  
    {vulnerability_report}



    ### Task:  
    1. **Analyze**:  
    - Understand the vulnerable function's purpose and key steps.  
    - Identify how the vulnerability (described in the report) violates the intended behavior or security constraints.  

    2. **Repair**:  
    - Propose a patch that:  
        - Addresses the root cause of the vulnerability at/near the sink point.  
        - Preserves the original functional purpose and key steps.  
        - Minimizes code changes to reduce side effects.  

    3. **Output**:  
    - **Strictly output a single JSON object** with two fields:  
        - `diff`: A unified diff patch (e.g., `diff --git a/file b/file`) showing **only** necessary changes.  
        - `report`: A concise explanation of why the patch resolves the vulnerability and `why it’s effective.  
    - Ensure:  
        - No markdown, additional text, or formatting outside the JSON.  
        - Valid JSON syntax (escape quotes if needed).  
    ### Output Schema:
    {expected_schema}
    ### Example Output:  
    {{  
    "diff": "diff --git a/example.c b/example.c\n--- a/example.c\n+++ b/example.c\n@@ -123,7 +123,7 @@\n     // Key step: Process user input\n-    strcpy(buffer, user_input);\n+    strncpy(buffer, user_input, sizeof(buffer) - 1);",  
    "report": ["Replaced `strcpy` with `strncpy` to prevent buffer overflow by enforcing a maximum copy length based on `buffer` size. This ensures input processing (key step) remains functional while bounding memory writes."  ,"The solution of the second vulnerability." ,...]
    }}  

    ---  
    **Your Response (ONLY JSON):**  
    """
    name:str="GeneralRepair"
    desc:str="This action repairs the vulnerable code with given context."
    async def run(self,code_text:str,vuln_report:VulnReport,read_report:ReadReport)->OverallRepair:
        service=LLMService() # Initialize the singleton service
        prompt = self.PROMPT_TEMPLATE.format(code_file=code_text,read_report=read_report.model_dump_json(),vulnerability_report=vuln_report.model_dump_json(),expected_schema=OverallRepair.model_json_schema())
        res=await service.generate_structured_async(prompt,OverallRepair)
        if not isinstance(res, OverallRepair):
            raise ValueError("Invalid response from GeneralRepair. Stop execution.")
        return res