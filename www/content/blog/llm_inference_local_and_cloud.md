---
title: "Ollama LLM Inference Local and Cloud"
description: "How to run large language models locally and in the cloud with Ollama"
date: 2026-01-24
lastmod: 2026-01-24
weight: 7
---
Ollama is a tool designed to host large language models (LLMs) locally on macOS, Linux, and Windows systems, offering OpenAI-compatible APIs for seamless integration with existing applications. By running models locally, Ollama eliminates the need for cloud-based services, ensuring privacy and reducing costs.
<!-- more -->
When you want to run large language models, you call Ollama—a local-first LLM runtime that runs models on your GPU or Apple Silicon, talks to remote cloud models, and exposes both its native API and an OpenAI‑compatible API for chat and embeddings.

*Resources:*
- [Ollama Official Website](https://ollama.com)
- [Ollama Documentation](https://github.com/ollama/ollama/tree/main/docs)
- [Ollama API Reference](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [OpenAI API Compatibility](https://github.com/ollama/ollama/blob/main/docs/openai.md)
- [Model Library](https://ollama.com/library)

***

{{<figure src="imgs/ollama_pic.png" width="100%" alt="Ollama" >}}


##### 1. Architecture: local, remote, hybrid

You call Ollama's daemon, which exposes an HTTP API at `http://127.0.0.1:11434` by default. You configure clients with `OLLAMA_HOST` to point either to this local daemon or a remote server, and you optionally set `OLLAMA_API_KEY` when using Ollama Cloud.

- Local-only:
    - You install Ollama on macOS, Linux, or Windows.
    - You pull a model: `ollama pull llama3.1`.
    - You access it via CLI (`ollama run llama3.1`) or HTTP (`/api/chat`, `/api/generate`, `/api/embed`).
- Remote server:
    - You run Ollama on a GPU box and expose `11434` behind TLS/reverse proxy.
    - You set `OLLAMA_HOST=https://your-server:11434` in clients or SDKs.
- Cloud:
    - You call Ollama Cloud directly via `https://ollama.com` as the host, with `OLLAMA_API_KEY` for auth.
- Hybrid:
    - You point tools at your local daemon for on-prem models, but you also provide `OLLAMA_API_KEY` so the same tooling routes to cloud models when you use a cloud model ID.

Example: in a config for an MCP server, you use hybrid mode with both `OLLAMA_HOST=http://127.0.0.1:11434` and an `OLLAMA_API_KEY` so local calls hit your machine while cloud model names are proxied to Ollama Cloud.

##### 2. Hardware: running models on GPU or Apple Silicon

When you run Ollama on Apple Silicon, you call the Metal Performance Shaders stack to offload to the GPU, giving you fast local inference with efficient memory use. On Linux/Windows GPU servers, you call GPU backends (via CUDA/DirectML depending on platform) to accelerate the same GGUF models.

- Model selection:
    - You choose smaller models (e.g. 7B) that fit comfortably into laptop‑class VRAM/Unified Memory.
    - You use quantized formats (e.g. Q4_K_M) for larger models to fit into constrained memory.
- Performance:
    - You get GPU acceleration that significantly improves token throughput versus pure CPU.
    - You benefit from Apple Silicon's unified memory and Metal GPU integration.

You don’t need to change API calls for GPU vs CPU; Ollama chooses the best execution path based on hardware and model configuration.

##### 3. Core native APIs: chat, generate, embeddings

Ollama’s “original” API is under `/api/*` on the daemon and is JSON‑over‑HTTP.

###### 3.1 Chat API (`/api/chat`)

You call this endpoint for multi‑turn conversations with roles.

Minimal non‑streaming example (curl):

```bash
curl http://localhost:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1",
    "messages": [
      { "role": "user", "content": "Explain RAG in one paragraph." }
    ],
    "stream": false
  }'
```

You send:

- `model`: model name or tag (local or cloud ID).
- `messages`: list of `{role, content}` (roles: `system`, `user`, `assistant`).
- Optional: `stream` (default true), `options` (temperature, top_k, etc.), `format` (for structured output).

You receive (non‑stream):

- `model`, `created_at`.
- `message` with `role` and `content`.
- `done`, token counts and timings.


###### 3.2 Generate API (`/api/generate`)

This endpoint is for single‑prompt completion, more “completion”‑style than chat.

Example:

```bash
curl http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1",
    "prompt": "Write a SQL query to list customers by revenue.",
    "stream": false
  }'
```

You pass `prompt` instead of `messages`. You receive similar response content, but with a `response` field containing the generated text, plus token counts and timings.

###### 3.3 Embeddings API (`/api/embed` and OpenAI `/v1/embeddings`)

You call Ollama's native embeddings endpoint at `/api/embed` or, for OpenAI‑compatibility, you call `/v1/embeddings`.

Native embeddings example:

```bash
curl http://localhost:11434/api/embed \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nomic-embed-text",
    "input": ["hello world", "another document"]
  }'
```

You receive `embeddings`, a list of float vectors, and metadata.

When you call the OpenAI‑compatible embeddings endpoint at `/v1/embeddings`, you use the OpenAI‑style payload (`input`, `model`), though some older discussions noted limitations (e.g., single input vs array) that have been iterated on over time.

##### 4. Using Ollama with cloud models

When you use Ollama Cloud, it effectively behaves like a remote Ollama host that speaks the same API as your local daemon.

###### 4.1 Direct cloud API

You can call `https://ollama.com` with your API key:

```bash
export OLLAMA_API_KEY=your_api_key

curl https://ollama.com/api/chat \
  -H "Authorization: Bearer $OLLAMA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-oss:120b",
    "messages": [
      { "role": "user", "content": "Summarize Ollama cloud in 3 bullet points." }
    ],
    "stream": false
  }'
```

In this mode:

- Host is `https://ollama.com`.
- Model name is a cloud model ID (e.g. `gpt-oss:...`).
- You don’t need any local daemon; everything runs in the cloud.


###### 4.2 Local daemon + cloud proxying (hybrid)

When you use many tools and SDKs, you can specify cloud model IDs while pointing to your local daemon; the daemon itself then proxies those calls to Ollama Cloud as needed. You typically:

- Keep `OLLAMA_HOST` pointing at your local daemon.
- Provide `OLLAMA_API_KEY` so cloud requests can be authenticated.
- Use cloud model IDs in `model` fields when you want the remote model; use local model names otherwise.

This lets you mix local and remote compute seamlessly with a single client or orchestration layer.

##### 5. OpenAI‑compatible API

When you use Ollama, it supports the OpenAI Chat Completions API and related semantics, so you can use existing OpenAI‑targeted tools against your local models (or cloud via hybrid).

###### 5.1 Chat Completions (`/v1/chat/completions`)

Example:

```bash
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1",
    "messages": [
      { "role": "system", "content": "You are a concise assistant." },
      { "role": "user", "content": "List 3 benefits of local LLMs." }
    ],
    "temperature": 0.3,
    "stream": false
  }'
```

This mirrors OpenAI’s JSON structure:

- `model`, `messages`, temperature/top_p, `stream`.
- Response has `id`, `object`, `choices` with `message`, and `usage` for token counts.

Because of this compatibility, you can reuse OpenAI‑aware SDKs and frameworks by just changing the base URL and model name.

###### 5.2 Embeddings (`/v1/embeddings`)

Ollama’s OpenAI compatibility page notes that embeddings support is provided via a `/v1/embeddings` endpoint, though historically it lagged behind chat in feature‑parity and had some constraints. The pattern is:

- POST to `/v1/embeddings` with `model` and `input`.
- Receive `data` array with `embedding` vectors and `usage`.

Frameworks like Elasticsearch’s “Inference API” show how they point their OpenAI‑style clients at an Ollama base URL to using this interface in RAG pipelines.

###### 5.3 Comparison: native vs OpenAI‑compatible

| Aspect | Native Ollama API (`/api/*`) | OpenAI‑compatible API (`/v1/*`) |
| :-- | :-- | :-- |
| Base paths | `/api/chat`, `/api/generate`, `/api/embed` | `/v1/chat/completions`, `/v1/embeddings` |
| Request shape | Ollama‑specific fields (`format`, `options`) | OpenAI schema (`messages`, `functions`, `tools`, etc.) |
| Client ecosystem | Ollama SDKs, direct HTTP | Any OpenAI‑aware SDK/tooling (Playground, RAG libs) |
| Feature lead | Often first for new Ollama features | Follows, focused on compatibility |
| Best for | Direct integration, structured output demos | Drop‑in replacement for OpenAI in existing apps |

##### 6. Structured output (JSON / JSON Schema)

Ollama can enforce structured JSON outputs using a `format` parameter, turning JSON Schema into a decoding grammar so that the model’s output conforms to your schema.

###### 6.1 Simple JSON mode (`"format": "json"`)

When you set `"format": "json"` on `/api/chat`, you constrain the model to emit valid JSON of arbitrary structure.

```bash
curl http://localhost:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1",
    "messages": [
      { "role": "user", "content": "Give me a short bio of Ada Lovelace." }
    ],
    "stream": false,
    "format": "json"
  }'
```

The `message.content` will be a valid JSON string that you can parse directly, even though you didn’t specify a schema.

###### 6.2 JSON Schema for fully structured outputs

When you pass a full JSON Schema as the `format` field, you require a specific shape.

Example with curl:

```bash
curl http://localhost:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1",
    "messages": [
      { "role": "user", "content": "Tell me about Canada." }
    ],
    "stream": false,
    "format": {
      "type": "object",
      "properties": {
        "name":      { "type": "string" },
        "capital":   { "type": "string" },
        "languages": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
      "required": ["name", "capital", "languages"]
    }
  }'
```

You'll receive JSON in `message.content` matching that schema, e.g.:

```json
{
  "name": "Canada",
  "capital": "Ottawa",
  "languages": ["English", "French"]
}
```

with the model forbidden from emitting structurally invalid content.

###### 6.3 Using Pydantic / typed models

When you use Python, the Ollama SDK integrates nicely with Pydantic: you pass `model_json_schema()` as `format`, then you validate the returned JSON with `model_validate_json`.

```python
from ollama import chat
from pydantic import BaseModel

class Country(BaseModel):
    name: str
    capital: str
    languages: list[str]

response = chat(
    model='llama3.1',
    messages=[{'role': 'user', 'content': 'Tell me about Canada.'}],
    format=Country.model_json_schema(),
)

country = Country.model_validate_json(response.message.content)
print(country)
```

Here, Ollama enforces the JSON schema during generation and Pydantic enforces it again during parsing, giving you strongly typed results in your code.

The same mechanism works with nested schemas (objects containing arrays of objects, optional fields, enums, etc.), and integrations like LangChain’s `langchain_ollama` default to using this structured output path for JSON schema guidance.

###### 6.4 Structured output with images

Structured outputs can be combined with vision models by attaching `images` to messages and providing an image‑description schema; the model’s response will be a JSON object conforming to that structure (e.g. listing detected objects, scene description, etc.). You'll find this useful for building consistent vision‑plus‑text pipelines where your downstream code assumes a fixed schema.

### Python code examples for Ollama chat with streaming

Here are Python examples for streaming chat with Ollama using both the official SDK and raw HTTP.

##### 1. Synchronous streaming with the Python SDK

```python
from ollama import chat

def stream_chat_sync():
    stream = chat(
        model='llama3.1',
        messages=[
            {'role': 'system', 'content': 'You are a concise assistant.'},
            {'role': 'user', 'content': 'Explain what an API is in simple terms.'},
        ],
        stream=True,  # enable streaming
    )

    full_text = []
    for chunk in stream:
        delta = chunk['message']['content']
        print(delta, end='', flush=True)
        full_text.append(delta)

    print()  # newline at end
    return ''.join(full_text)

if __name__ == '__main__':
    answer = stream_chat_sync()
```

The SDK returns an iterator when `stream=True`; each `chunk` is a dict containing a `message` with partial `content` that you can print or buffer.

##### 2. Asynchronous streaming with the Python SDK

```python
import asyncio
from ollama import AsyncClient

async def stream_chat_async():
    client = AsyncClient()
    message = {'role': 'user', 'content': 'Why is the sky blue?'}
    full_text = []

    async for part in await client.chat(
        model='llama3.1',
        messages=[message],
        stream=True,
    ):
        delta = part['message']['content']
        print(delta, end='', flush=True)
        full_text.append(delta)

    print()
    return ''.join(full_text)

if __name__ == '__main__':
    asyncio.run(stream_chat_async())
```

When using `AsyncClient`, `stream=True` makes `chat` return an async generator you can iterate with `async for` to consume chunks as they arrive.

##### 3. Streaming via raw HTTP (`requests` + `/api/chat`)

If you prefer not to use the SDK, you can stream from the native REST API using `requests` with `stream=True`.

```python
import requests
import json

def stream_chat_http(messages, model: str = 'llama3.1') -> str:
    url = 'http://localhost:11434/api/chat'
    payload = {
        'model': model,
        'messages': messages,
        'stream': True,
    }

    full_response = []
    with requests.post(url, json=payload, stream=True) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines():
            if not line:
                continue
            chunk = json.loads(line)
            content = chunk.get('message', {}).get('content', '')
            if content:
                print(content, end='', flush=True)
                full_response.append(content)
            if chunk.get('done'):
                print()
                break

    return ''.join(full_response)

if __name__ == '__main__':
    msgs = [
        {'role': 'system', 'content': 'You are a helpful coding assistant.'},
        {'role': 'user', 'content': 'What is REST?'},
    ]
    full = stream_chat_http(msgs)
```

In this pattern, each line is a JSON object from Ollama; you parse it, read the incremental `message.content`, and stop when `done` is `true`.


### Curl and Python example side by side

Below are Python `requests` equivalents for each earlier `curl` example: chat, generate, embeddings, cloud chat, and structured output. I’ll assume `http://localhost:11434` for local and `https://ollama.com` for cloud; adjust as needed.


##### 1. `/api/chat` (basic non‑streaming chat)

| Original curl | Python with `requests` |
|---------------|------------------------|

**Original curl**
```bash
curl http://localhost:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1",
    "messages": [
      { "role": "user", "content": "Explain RAG in one paragraph." }
    ],
    "stream": false
  }'
```

**Python with `requests`**
```python
import requests

def chat_basic():
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "llama3.1",
        "messages": [
            {"role": "user", "content": "Explain RAG in one paragraph."},
        ],
        "stream": False,
    }

    resp = requests.post(url, json=payload)
    resp.raise_for_status()

    data = resp.json()
    print(data["message"]["content"])
    return data

if __name__ == "__main__":
    chat_basic()
```

This matches the non‑streaming behavior of the curl example and reads the final JSON response.


##### 2. `/api/generate` (single‑prompt completion)

**Original curl**

```bash
curl http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1",
    "prompt": "Write a SQL query to list customers by revenue.",
    "stream": false
  }'
```

**Python with `requests`**

```python
import requests

def generate_basic():
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3.1",
        "prompt": "Write a SQL query to list customers by revenue.",
        "stream": False,
    }

    resp = requests.post(url, json=payload)
    resp.raise_for_status()

    data = resp.json()
    print(data["response"])
    return data

if __name__ == "__main__":
    generate_basic()
```

Here `response["response"]` contains the full generated text for the prompt.


##### 3. `/api/embed` (native embeddings)

**Original curl**

```bash
curl http://localhost:11434/api/embed \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nomic-embed-text",
    "input": ["hello world", "another document"]
  }'
```

**Python with `requests`**

```python
import requests

def embed_basic():
    url = "http://localhost:11434/api/embed"
    payload = {
        "model": "nomic-embed-text",
        "input": ["hello world", "another document"],
    }

    resp = requests.post(url, json=payload)
    resp.raise_for_status()

    data = resp.json()
    embeddings = data["embeddings"]  # list of vectors
    print("Got", len(embeddings), "embeddings of dim", len(embeddings))
    return embeddings

if __name__ == "__main__":
    embed_basic()
```

The JSON response includes an `embeddings` array with one vector per input string.

##### 4. Cloud chat via `https://ollama.com/api/chat`

**Original curl**

```bash
export OLLAMA_API_KEY=your_api_key

curl https://ollama.com/api/chat \
  -H "Authorization: Bearer $OLLAMA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-oss:120b",
    "messages": [
      { "role": "user", "content": "Summarize Ollama cloud in 3 bullet points." }
    ],
    "stream": false
  }'
```

**Python with `requests`**

```python
import os
import requests

def cloud_chat():
    api_key = os.environ["OLLAMA_API_KEY"]
    url = "https://ollama.com/api/chat"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "gpt-oss:120b",
        "messages": [
            {
                "role": "user",
                "content": "Summarize Ollama cloud in 3 bullet points.",
            }
        ],
        "stream": False,
    }

    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()

    data = resp.json()
    print(data["message"]["content"])
    return data

if __name__ == "__main__":
    cloud_chat()
```

This uses the same JSON structure as local `/api/chat`, but points to the cloud host and includes a Bearer token.


##### 5. Structured output with JSON Schema (`/api/chat`)

**Original curl**

```bash
curl http://localhost:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1",
    "messages": [
      { "role": "user", "content": "Tell me about Canada." }
    ],
    "stream": false,
    "format": {
      "type": "object",
      "properties": {
        "name":      { "type": "string" },
        "capital":   { "type": "string" },
        "languages": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
      "required": ["name", "capital", "languages"]
    }
  }'
```

**Python with `requests`**

```python
import json
import requests

def chat_structured():
    url = "http://localhost:11434/api/chat"

    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "capital": {"type": "string"},
            "languages": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
        "required": ["name", "capital", "languages"],
    }

    payload = {
        "model": "llama3.1",
        "messages": [
            {"role": "user", "content": "Tell me about Canada."},
        ],
        "stream": False,
        "format": schema,
    }

    resp = requests.post(url, json=payload)
    resp.raise_for_status()

    data = resp.json()
    # content itself is a JSON string
    content = data["message"]["content"]
    obj = json.loads(content)

    print(obj)
    print("Capital:", obj["capital"])
    return obj

if __name__ == "__main__":
    chat_structured()
```

Here `format` carries the JSON Schema and Ollama constrains generation to match it; you then parse `message.content` as JSON in Python.


If you want, I can also mirror these for the OpenAI‑compatible routes (`/v1/chat/completions`, `/v1/embeddings`) using `requests.post(...)` against the same base URL.


**References**
- https://docs.ollama.com/api/introduction
- https://docs.ollama.com/capabilities/structured-outputs
- https://docs.ollama.com/cloud
- https://ollama.com/blog/openai-compatibility
- https://ollama.com/blog/streaming-tool
- https://ollama.com/blog/structured-outputs
- https://github.com/ollama/ollama-python
- https://mcpservers.org/servers/rawveg/ollama-mcp
- https://www.cohorte.co/blog/using-ollama-with-python-step-by-step-guide
- https://www.glukhov.org/llm-hosting/ollama/ollama-python-examples/
- https://www.glukhov.org/post/2025/10/ollama-python-examples/
