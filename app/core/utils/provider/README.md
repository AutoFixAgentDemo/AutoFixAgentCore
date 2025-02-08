# LLM Client Providers

A flexible and extensible abstraction layer for Large Language Model (LLM) integrations, providing structured output handling and validation through Pydantic BaseModel. This package implements a factory pattern to dynamically select and initialize different LLM providers based on configuration.

This package is designed specifically for application-layer implementations and serves as a complementary client to the core MetaGPT provider system.


> [!IMPORTANT]
> The custom client is intended for use only in application layer components (roles, actions, etc). Internal MetaGPT components will continue to use the existing client implementation in `app/base/core/provider`.

## To setup a custom LLM Client 
1. Inherit from `BaseLLMClient` and implement the required methods
2. Register your LLM Client by `LLMFactory.register_llm("custom_llm", CustomLLMClient)`
3. Configure your LLM backend config in `settings.toml` and `.secrect.toml`
4. Also, config well for MetaGPT in `app/base/core/provider`.
