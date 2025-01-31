from typing import List

from pydantic import BaseModel

class OverallRepair(BaseModel):
    """
    A BaseModel class for overall repair to fix all vulnerbilities mentioned in the input."""
    """

    Example:
    {
      "diff": "diff --git a/example.c b/example.c\n--- a/example.c\n+++ b/example.c\n@@ -123,7 +123,7 @@\n     // Key step: Process user input\n-    strcpy(buffer, user_input);\n+    strncpy(buffer, user_input, sizeof(buffer) - 1);",// The general diff in the whole code file
      "report": ["Replaced `strcpy` with `strncpy` to prevent buffer overflow by enforcing a maximum copy length based on `buffer` size. This ensures input processing (key step) remains functional while bounding memory writes.","Another explain if multi vulnerbilities are found in the vulnerability report."]
    }

    """
    diff: str
    report: List[str]