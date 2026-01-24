from pydantic import BaseModel
from typing import List, Optional, Any

class MessagePart(BaseModel):
    type: str
    text: Optional[str] = None

class ChatMessage(BaseModel):
    id: str
    role: str
    content: Optional[str] = None
    parts: Optional[List[MessagePart]] = None

class ChatRequestSchema(BaseModel):
    user_id: str
    session_id: str
    messages: List[ChatMessage]
    code: str
    language: str
    problem_description: str

class ChatResponseSchema(BaseModel):
    response: str

