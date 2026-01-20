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
    code: Optional[str] = None
    language: Optional[str] = None
    problem_description: Optional[str] = None
    
class ChatResponseSchema(BaseModel):
    response: str

