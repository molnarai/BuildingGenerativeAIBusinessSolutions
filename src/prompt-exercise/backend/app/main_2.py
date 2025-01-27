from typing import List, Dict, Any
import os
import time
import json
import asyncio
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi import Depends, Response
from fastapi.security import HTTPBearer


from pydantic import BaseModel
# from langchain.llms import Ollama
from langchain_community.llms import Ollama
# from langchain_ollama import OllamaLLM
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import HumanMessage, SystemMessage, AIMessage, ChatMessage
# from langchain.chat_models import ChatOllama
# from langchain_community.chat_models import ChatOllama
from langchain_ollama import ChatOllama
# from chroma_client import ChromaClient # Adding Chroma Class

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


ollama_base_url = os.getenv("OLLAMA_BASE_URL")
db_host = os.getenv("DB_HOST")
chromadb_port = os.getenv("CHROMADB_PORT")

# chroma_client = ChromaClient(host='10.230.100.212', port=17026)  # Initialize ChromaDB client
# chroma_client = ChromaClient(host=db_host, port=chromadb_port)  # Initialize ChromaDB client

class StreamingCallbackHandler(BaseCallbackHandler):
    def __init__(self):
        self.tokens = []
        self.done = asyncio.Event()

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.tokens.append(token)

    def on_llm_end(self, *args, **kwargs) -> None:
        self.done.set()

class CompletionRequest(BaseModel):
    model: str
    prompt: str
    max_tokens: int = 100
    temperature: float = 0.7
    stream: bool = False

class ChatCompletionRequest(BaseModel):
    model: str
    messages: list
    max_tokens: int = 100
    temperature: float = 0.7
    stream: bool = False


async def stream_tokens(callback: StreamingCallbackHandler):
    while not callback.done.is_set() or callback.tokens:
        if callback.tokens:
            token = callback.tokens.pop(0)
            yield f"data: {json.dumps({'choices': [{'delta': {'content': token}}]})}\n\n"
        else:
            await asyncio.sleep(0.1)
    yield "data: [DONE]\n\n"

@app.post("/v1/completions")
async def create_completion(request: CompletionRequest):
    callback = StreamingCallbackHandler()
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

@app.post("/v1/chat/completions")
async def create_chat_completion(request: ChatCompletionRequest):
    callback = StreamingCallbackHandler()
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
    

#    ___  _ _                         __  __           _      _     
#   / _ \| | | __ _ _ __ ___   __ _  |  \/  | ___   __| | ___| |___ 
#  | | | | | |/ _` | '_ ` _ \ / _` | | |\/| |/ _ \ / _` |/ _ \ / __|
#  | |_| | | | (_| | | | | | | (_| | | |  | | (_) | (_| |  __/ \__ \
#   \___/|_|_|\__,_|_| |_| |_|\__,_| |_|  |_|\___/ \__,_|\___|_|___/
                                                                  

@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [
            {
                "id": "llama3.1",
                "object": "model",
                "created": 1700000000,
                "owned_by": "me"
            }
        ]
    }



#   _   _                    _         _   _                _   _           _   _             
#  | | | |___  ___ _ __     / \  _   _| |_| |__   ___ _ __ | |_(_) ___ __ _| |_(_) ___  _ __  
#  | | | / __|/ _ \ '__|   / _ \| | | | __| '_ \ / _ \ '_ \| __| |/ __/ _` | __| |/ _ \| '_ \ 
#  | |_| \__ \  __/ |     / ___ \ |_| | |_| | | |  __/ | | | |_| | (_| (_| | |_| | (_) | | | |
#   \___/|___/\___|_|    /_/   \_\__,_|\__|_| |_|\___|_| |_|\__|_|\___\__,_|\__|_|\___/|_| |_|
                                                                                            
security = HTTPBearer()

async def verify_token(response: Response, token: str = Depends(security)):
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid token or token has expired"
        )
    return token

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(request: LoginRequest):
    if request.username == "admin" and request.password == "admin":
        # create a random token and save in Session
        token = os.urandom(12).hex()
        
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get("/user")
async def get_user(token: str = Depends(security)):
    # check if token is valid
    if token.credentials == "admin":
        return {"username": "XXXXX"}
    else:
        raise HTTPException(status_code=401, detail="Invalid token")
    

@app.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful"}


#   __  __       _       
#  |  \/  | __ _(_)_ __  
#  | |\/| |/ _` | | '_ \ 
#  | |  | | (_| | | | | |
#  |_|  |_|\__,_|_|_| |_|
                       


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)