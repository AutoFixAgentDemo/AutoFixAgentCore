from autogen import AssistantAgent, UserProxyAgent

config_list = [
    {
        "model": "qwen2.5:32b",
        "base_url": "http://222.20.126.175:8100/v1",
        "api_key": "ollama",
    }
]

assistant = AssistantAgent("assistant", llm_config={"config_list": config_list})

user_proxy = UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding", "use_docker": False})

# Start the chat
user_proxy.initiate_chat(
    assistant,
    message="Say hello to all other people!",
)
