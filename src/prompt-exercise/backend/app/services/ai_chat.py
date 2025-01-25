from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage
from langchain.callbacks.base import BaseCallbackHandler
import asyncio
import os

class StreamingCallbackHandler(BaseCallbackHandler):
    def __init__(self):
        self.tokens = []
        self.done = asyncio.Event()

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.tokens.append(token)

    def on_llm_end(self, *args, **kwargs) -> None:
        self.done.set()

async def generate_chat_response(messages, temperature, max_tokens, stream=False):
    callback = StreamingCallbackHandler()
    chat_model = ChatOllama(
        base_url=os.getenv("OLLAMA_BASE_URL"),
        model="llama3.1",
        callbacks=[callback],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    
    messages = [HumanMessage(content=msg["content"]) for msg in messages if msg["role"] == "user"]
    return await chat_model.agenerate([messages])
