from typing import List

from pydantic import BaseModel

class SingleVerify(BaseModel):
    """
    To define the verification result of a single vulnerability.
    """
    verify_status:bool
    verify_message:str

class OverallVerify(BaseModel):
    """
    A BaseModel class for overall verification result of the code.
    """
    verify_reports:List[SingleVerify]
    
    