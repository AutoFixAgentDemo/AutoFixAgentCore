# AutoFixAgentCore

The AutoFixAgent is a RAG and multi-agents based APR tool using [MetaGPT](https://docs.deepwisdom.ai/main/zh/)
and [LightRAG](https://github.com/HKUDS/LightRAG).

## Prerequisites

This proj is a part of the whole project. You must do those before running this project.

> [!IMPORTANT]
> This project is running under `app` directory.

## Install

### Config the LLM backend by ollama

> [!NOTE]
> Still on work

Copy the file `app/core/config/config2.example.yaml` to `app/core/config/config2.yaml`, then modify it to include your own LLM source. Refer to MetaGPT's documentation for proper configuration within the MetaGPT framework.

Then initialize the independent configuration service by `dynaconf`:

```shell
cp .secrect.example.toml .secrets.toml 
```

Store sensitive credentials like `api_key` in `.secrets.toml` and configuration settings in `settings.toml`. Maintain separate files for security.

> [!IMPORTANT]
> Always provide a value for the `api_key` field, even if the backend (e.g., Ollama) does not require a valid API key. This is because the `instructor` library uses this field to populate the bearer token. Omitting it or leaving it empty may result in a `400 Bad Request` error when requesting a structured response.

> [!TIP]
> For detailed examples and instructions on implementing a custom client (other than `OllamaClient`) and using it, refer to `app/llm_test.py` and `app/core/utils/provider/ollama.py`.

### Install the dependencies

```shell
conda create -f environments.yaml
```

## Usage
### Run the example to test the reachbility of metagpt framework

```shell
cd app
python3 example.py
```

### Run the example to test the custom LLM client

```shell
cd app
python3 llm_test.py
```

### Run core client isolately

```shell
cd app
python3  cli_core.py --help
```


## NOTE

Ref https://www.cnblogs.com/wuhuacong/p/18380808 to organize

