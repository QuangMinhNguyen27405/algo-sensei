from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
import json

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
    
    # Debug: Log the incoming request
    print(f"Received chat request: user_id={request.user_id}, session_id={request.session_id}")
    print(f"Messages count: {len(request.messages)}")
    print(f"Has code: {bool(request.code)}, language: {request.language}")
    
    return StreamingResponse(
        agent_service.stream_chat(
            user_id=request.user_id,
            session_id=request.session_id,
            messages=request.messages,
            code=request.code,
            language=request.language,
            problem_description=request.problem_description
        )
    )
    
@router.post("/chat-test")
async def chat_endpoint_test(req: Request):
    import uuid
    
    data = await req.json()
    messages = data.get("messages", [])
    
    # Convert messages to simple text format for Google SDK
    # Frontend sends: [{'role': 'user', 'parts': [{'type': 'text', 'text': '...'}], 'id': '...'}]
    # Google SDK expects: simple text string or proper Content objects
    converted_messages = []
    for msg in messages:
        if isinstance(msg, dict) and 'parts' in msg:
            # Extract text from parts
            text_parts = []
            for part in msg.get('parts', []):
                if isinstance(part, dict) and 'text' in part:
                    text_parts.append(part['text'])
            if text_parts:
                converted_messages.append(' '.join(text_parts))
    
    # Combine all messages into one prompt
    prompt = ' '.join(converted_messages) if converted_messages else "Hello"
    
    async def generate():
        # Generate unique IDs for this message
        message_id = str(uuid.uuid4())
        text_id = str(uuid.uuid4())
        
        # Send message start
        yield f'data: {json.dumps({"type": "start", "messageId": message_id})}\n\n'
        
        # Send start step
        yield f'data: {json.dumps({"type": "start-step"})}\n\n'
        
        # Send text start
        yield f'data: {json.dumps({"type": "text-start", "id": text_id})}\n\n'
        
        # Using the async client for streaming
        stream = await client.aio.models.generate_content_stream(
            model='gemini-2.0-flash-exp',
            contents=prompt,
        )
        
        async for chunk in stream:
            if chunk.text:
                # Send text delta
                yield f'data: {json.dumps({"type": "text-delta", "id": text_id, "delta": chunk.text})}\n\n'
        
        # Send text end
        yield f'data: {json.dumps({"type": "text-end", "id": text_id})}\n\n'
        
        # Send finish step
        yield f'data: {json.dumps({"type": "finish-step"})}\n\n'
        
        # Send finish message
        yield f'data: {json.dumps({"type": "finish"})}\n\n'
        
        # Send stream termination
        yield 'data: [DONE]\n\n'

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream",
            "x-vercel-ai-ui-message-stream": "v1",
            "X-Content-Type-Options": "nosniff",
        }
    )