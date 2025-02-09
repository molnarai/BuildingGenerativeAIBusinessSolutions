---
draft: false
title: CORS for Local LLM Providers
weight: 29
description: For hosting LLMs locally with Ollama or LM Studio you need to enable Cross-Origin Resource Sharing (CORS)
---
Cross-origin resource sharing (CORS) is a mechanism for integrating applications. CORS defines a way for client web applications that are loaded in one domain to interact with resources in a different domain. This configuration is needed to allow local model providers to server web-applications what were loaded from a different site.

## Local Ollama Server
If you want to use Ollama local OpenAI compitable API through a browser based tool, you need to allow CORS. Follow these instructions https://objectgraph.com/blog/ollama-cors/


## Local LM Studio

Enable CORS in the server settings:

![LM Studio Settings](../lm_studio_server_settings.png)