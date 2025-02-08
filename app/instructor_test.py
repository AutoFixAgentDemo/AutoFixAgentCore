"""
This file tests the useability of the instructor lib(https://python.useinstructor.com/).

Usage:
cd app
python instructor_test.py

Expected output:
{"name":"Jason","age":25}

"""
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List
import instructor

class ExtractUser(BaseModel):
    name: str
    age: int

client = instructor.from_openai(
    OpenAI(
        base_url="http://172.17.0.16:11434/v1",
        api_key="NA",
    ),
    mode=instructor.Mode.JSON,
)

resp = client.chat.completions.create(
    model="qwen2.5:72b",
    messages=[
        {
            "role": "user",
            "content": "Extract Jason is 25 years old.",
        }
    ],
    response_model=ExtractUser,
)
assert resp.name == "Jason"
assert resp.age == 25
print(resp.model_dump_json())