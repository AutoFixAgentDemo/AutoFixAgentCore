"""
This is the file to test the reachability of the LLM API asynchronously.
"""

import asyncio
from core.utils.service import LLMService
from pydantic import BaseModel
from core.utils.provider.ollama import OllamaClient # NOTE: Import the OllamaClient class from the ollama.py file to register automatically.


class ExampleModel(BaseModel):
    name: str
    score: float


# 测试异步 generate_structured 方法
async def main():
    # 初始化服务
    service2 = LLMService()

    print(f"service2 config: {service2.config}")

    # 使用异步 generate_structured_async 生成结构化数据
    print(f"testing service2")
    print(f"service2 uses {service2.list_available_llms()}")
    res = await service2.generate_structured_async(
        prompt="Tom got 90 points in the exam. Convert the fact to a json with the following format. Respond using JSON.",
        expected_model=ExampleModel,
    )
    print(res, type(res))


# 运行异步测试
if __name__ == "__main__":
    asyncio.run(main())