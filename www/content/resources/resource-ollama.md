---
draft: false
title: Ollama
weight: 30
description: An Application Programming Interface (API) is a set of rules and protocols that enables communication between different software systems, acting as a bridge to facilitate data exchange and interaction.
---
[Ollama]( https://ollama.com) is a tool designed to host large language models (LLMs) locally on macOS, Linux, and Windows systems, offering OpenAI-compatible APIs for seamless integration with existing applications. By running models locally, Ollama eliminates the need for cloud-based services, ensuring privacy and reducing costs.
<!-- more -->
Its OpenAI-compatible API allows developers to use the same request formats as OpenAI's Chat Completions API, making it easy to switch between providers or run applications locally without modifying code. Users can interact with the API through HTTP requests or libraries like Python's `openai` library by simply changing the base URL to `http://localhost:11434`.

To install Ollama, users visit the official website, download the installer for their operating system, and follow straightforward installation steps. On **Windows**, users run the `.exe` file and use PowerShell or Command Prompt to manage models. On **macOS**, users download a `.zip` file, move it to the Applications folder, and use Terminal to interact with models. For **Linux**, users execute a shell script from the command line to install Ollama and manage models. Once installed, users can download models using commands like `ollama pull llama2`.

Ollama supports a variety of open-source models, including Llama 2 (7B, 13B, 70B), Llama 3, Mistral (7B), WizardLM-2 (7B), Code Llama (7B), Vicuna (7B), and Phi-3 Mini (3.8B). These models cover tasks such as text generation, coding assistance, and conversational AI. Users can also customize or bundle their own GGUF-formatted models for specific needs. With its ease of setup and OpenAI compatibility, Ollama is a powerful solution for hosting LLMs locally while maintaining flexibility and privacy.


**References:**

- [Ollama Library](https://ollama.com/library)
- [Ollama Comaptibility with OpenAI](https://ollama.com/blog/openai-compatibility)
- [Ollama Download for Windows, mac OS, Linux](https://ollama.com/download)
- [Install an AI LLM on Your Computer: A Step-by-Step Guide](https://www.adventuresincre.com/how-to-install-llm-locally/)
- [How to setup Ollama on Windows](https://www.yuchenkuang.com/ai-tools/useful-ai-tools/how-to-setup-ollama-on-windows)
- [Using Ollama to host an LLM on CPU-only equipment to enable a local chatbot and OpenAI-compatible API server](https://blog.gordonbuchan.com/blog/index.php/2025/01/11/using-ollama-to-host-an-llm-on-cpu-only-equipment-to-enable-a-local-chatbot-and-openai-compatible-api-server/)
- [How to Run Open Source LLMs on Your Own Computer Using Ollama](https://www.freecodecamp.org/news/how-to-run-open-source-llms-on-your-own-computer-using-ollama/)

