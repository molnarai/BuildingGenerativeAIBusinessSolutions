from fastapi import APIRouter, Depends
from services import ai_chat as chat_service
from models.ai_chat import CompletionRequest, ChatCompletionRequest
from utils.security import security
import json

import os
import time
import json
import asyncio
# from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
# from pydantic import BaseModel
# from langchain.llms import Ollama
from langchain_community.llms import Ollama
# from langchain_ollama import OllamaLLM
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import HumanMessage, SystemMessage, AIMessage, ChatMessage
# from langchain.chat_models import ChatOllama
# from langchain_community.chat_models import ChatOllama
from langchain_ollama import ChatOllama
import requests


ollama_base_url = os.getenv("EXTERNAL_OLLAMA_BASE_URL")
assert len(ollama_base_url) > 0, "EXTERNAL_OLLAMA_BASE_URL is not set"

router = APIRouter()

@router.get("/v1/models")
async def list_models():
    url = f"{ollama_base_url}/v1/models"
    response = requests.get(url)
    return response.json()


async def stream_tokens(callback: chat_service.StreamingCallbackHandler):
    while not callback.done.is_set() or callback.tokens:
        if callback.tokens:
            token = callback.tokens.pop(0)
            yield f"data: {json.dumps({'choices': [{'delta': {'content': token}}]})}\n\n"
        else:
            await asyncio.sleep(0.1)
    yield "data: [DONE]\n\n"



@router.post("/v1/completions")
async def create_completion(request: CompletionRequest):
    callback = chat_service.StreamingCallbackHandler()
    llm = Ollama(
        base_url=ollama_base_url,
        model="llama3.1",
        callbacks=[callback],
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )

    try:
        if request.stream:
            asyncio.create_task(llm.agenerate([request.prompt]))
            return StreamingResponse(stream_tokens(callback), media_type="text/event-stream")
        else:
            response = await llm.agenerate([request.prompt])
            return {
                "id": "cmpl-" + os.urandom(12).hex(),
                "object": "text_completion",
                "created": int(time.time()),
                "model": request.model,
                "choices": [
                    {
                        "text": response.generations[0][0].text,
                        "index": 0,
                        "logprobs": None,
                        "finish_reason": "stop"
                    }
                ],
                "usage": {
                    "prompt_tokens": len(request.prompt.split()),
                    "completion_tokens": len(response.generations[0][0].text.split()),
                    "total_tokens": len(request.prompt.split()) + len(response.generations[0][0].text.split())
                }
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/v1/chat/completions")
async def create_chat_completion(request: ChatCompletionRequest):
    callback = chat_service.StreamingCallbackHandler()
    chat_model = ChatOllama(
        base_url=ollama_base_url,
        model="llama3.1",
        callbacks=[callback],
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )

    try:
        messages = [HumanMessage(content=msg["content"]) for msg in request.messages if msg["role"] == "user"]
        
        if request.stream:
            asyncio.create_task(chat_model.agenerate([messages]))
            return StreamingResponse(stream_tokens(callback), media_type="text/event-stream")
        else:
            response = await chat_model.agenerate([messages])
            return {
                "id": "chatcmpl-" + os.urandom(12).hex(),
                "object": "chat.completion",
                "created": int(time.time()),
                "model": request.model,
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": response.generations[0][0].text
                        },
                        "finish_reason": "stop"
                    }
                ],
                "usage": {
                    "prompt_tokens": sum(len(msg.content.split()) for msg in messages),
                    "completion_tokens": len(response.generations[0][0].text.split()),
                    "total_tokens": sum(len(msg.content.split()) for msg in messages) + len(response.generations[0][0].text.split())
                }
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
