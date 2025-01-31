"""
Defines a class that represents read reports for a single run.
"""

from pydantic import BaseModel
from typing import List

class SingleFuncReport(BaseModel):
    """
    SingleFuncReport model

    Example:
    {
    "functionName": "Name of the function or the method",
      "functionPurpose": "Short explanation of the function's purpose",
      "functionImplementation": ["A list of key steps on how the function is or should be implemented"]
    }

    """
    functionName: str
    functionPurpose: str
    functionImplementation: List[str]

class ReadReport(BaseModel):
    """
    ReadReport model which may contain multiple SingleFuncReport

    Example:
    {
      "functionReports": [
        {
          "functionName": "Name of the function or the method",
          "functionPurpose": "Short explanation of the function's purpose",
          "functionImplementation": ["A list of key steps on how the function is or should be implemented"]
        }
      ]
    }

    """

    functionReports: List[SingleFuncReport]