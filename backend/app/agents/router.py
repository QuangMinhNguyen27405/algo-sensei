from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
import json
import uuid

from google import genai
from app.agents.schemas import ChatRequestSchema
from app.agents.service import AgentService
from app.agents.dependency import get_agent_service
from app.config.settings import settings

client = genai.Client(api_key=settings.google_api_key)

router = APIRouter(
    prefix="/agent",
    tags=["agent"]
)

@router.post("/chat")
async def chat_endpoint(
    request: ChatRequestSchema,
    agent_service: AgentService = Depends(get_agent_service)
):
    """
    Chat endpoint compatible with AI SDK streaming format.
    Receives messages array and optional code context.
    """
    
    return StreamingResponse(
        agent_service.stream_chat(
            user_id=request.user_id,
            session_id=request.session_id,
            messages=request.messages,
            code=request.code,
            language=request.language,
            problem_description=request.problem_description
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream",
            "x-vercel-ai-ui-message-stream": "v1",
            "X-Content-Type-Options": "nosniff",
        }
    )
    
