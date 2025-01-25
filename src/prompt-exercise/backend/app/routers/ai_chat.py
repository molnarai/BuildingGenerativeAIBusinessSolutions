from fastapi import APIRouter, Depends
from ..services import ai_chat as chat_service
from ..models.chat import CompletionRequest, ChatCompletionRequest
from ..utils.security import security

router = APIRouter()

@router.post("/v1/completions")
async def create_completion(
    request: CompletionRequest,
    token: str = Depends(security)
):
    # Implementation here
    pass

@router.post("/v1/chat/completions")
async def create_chat_completion(
    request: ChatCompletionRequest,
    token: str = Depends(security)
):
    # Implementation here
    pass
