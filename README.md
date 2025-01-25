# AutoFixAgentCore

The AutoFixAgent is a RAG and multi-agents based APR tool using [MetaGPT](https://docs.deepwisdom.ai/main/zh/)
and [LightRAG](https://github.com/HKUDS/LightRAG).

## Prerequisites

This proj is a part of the whole project. You must do those before running this project.

## Install

### Config the LLM backend by ollama

[TBD]

Copy `app/core/config/config2.example.yaml` to `app/core/config/config2.yaml` and overwrite it with your own LLM source
referring MetaGPT's document

### Install the dependencies

#### Automatically

```shell
conda create -f environments.yaml
```
#### Create an conda env from the brand new manually

```shell
conda  create -n autofix python=3.9
conda activate autofix 
conda install -y gymnasium fire
pip install --upgrade metagpt
```

## NOTE

Ref https://www.cnblogs.com/wuhuacong/p/18380808 to organize