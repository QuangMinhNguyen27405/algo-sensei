"""Service layer for agent-related operations."""
import json
from typing import List, AsyncGenerator
import time
import uuid
from google.adk.sessions import InMemorySessionService
from google.adk.events import Event, EventActions
from google.adk.agents.run_config import RunConfig, StreamingMode


from google.adk import Runner
from google.genai.types import Content, Part

from app.agents.schemas import ChatMessage


class AgentService:
    """Service for handling LeetCode analysis using AI agents."""
    
    def __init__(self, runner: Runner, session_service: InMemorySessionService):
        """Initialize the AgentService with required dependencies.
        
        Args:
            runner: The Runner instance for executing agents
            session_service: Shared session service for maintaining tab sessions
        """
        self.runner = runner
        self.session_service = session_service
    
    def _extract_message_text(self, message: ChatMessage) -> str:
        """Extract text content from a message."""
        if message.content:
            return message.content
        if message.parts:
            return " ".join(
                part.text for part in message.parts 
                if part.type == "text" and part.text
            )
        return ""
    
    async def stream_chat(
        self, 
        user_id: str,
        session_id: str,
        messages: List[ChatMessage],
        code: str,
        language: str,
        problem_description: str
    ) -> AsyncGenerator[str, None]:
        """
        Stream chat responses compatible with AI SDK UI Message Stream format.
        
        Args:
            messages: List of chat messages
            code: Optional code context from the editor
            language: Optional programming language
            problem_description: Optional problem description
            
        Yields:
            Streaming response chunks in AI SDK format
        """
        
        if not messages:
            yield 'e:{"error":"No messages provided"}\n'
            return
        
        prompt = ""
        for msg in reversed(messages):
            if msg.role == "user":
                text_parts = []
                if msg.parts:
                    for part in msg.parts:
                        if part.type == "text" and part.text:
                            text_parts.append(part.text)
                
                if text_parts:
                    prompt = ' '.join(text_parts)
                    break
        
        if not prompt:
            prompt = "Hello"
        
        # Create or get existing session
        existing_session = await self.session_service.get_session(
            app_name="algo_sensei",
            user_id=user_id,
            session_id=session_id
        )
        if existing_session:
            # Update session state with code
            state_changes: dict[str, object] = {
                "code": code,
                "language": language,
            }
            actions_with_update = EventActions(state_delta=state_changes)
            system_event = Event(
                invocation_id="inv_login_update",
                author="system",
                actions=actions_with_update,
                timestamp=time.time(),
            )
            await self.session_service.append_event(existing_session, system_event)
        else:
            # Create new session with initial state
            try:
                session = await self.session_service.create_session(
                    app_name="algo_sensei",
                    user_id=user_id,
                    session_id=session_id
                )
                initial_state: dict[str, object] = {
                    "problem_description": problem_description,
                    "code": code,
                    "language": language,
                }
                actions_with_update = EventActions(state_delta=initial_state)
                system_event = Event(
                    invocation_id="inv_login_update",
                    author="system",
                    actions=actions_with_update,
                    timestamp=time.time(),
                )

                await self.session_service.append_event(session, system_event)

            except Exception:
                yield 'e:{"error":"Failed to create session"}\n'
                return
        
        message_content = Content(
            parts=[Part(text=prompt)],
            role="user"
        )
        
        try:
            print(f"Starting Google ADK runner for session: {session_id}")
            
            message_id = str(uuid.uuid4())
            text_id = str(uuid.uuid4())
            
            yield f'data: {json.dumps({"type": "start", "messageId": message_id})}\n\n'
            
            yield f'data: {json.dumps({"type": "start-step"})}\n\n'
            
            yield f'data: {json.dumps({"type": "text-start", "id": text_id})}\n\n'

            print(message_content)

            stream = self.runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=message_content,
                run_config=RunConfig(
                    streaming_mode=StreamingMode.SSE,
                    max_llm_calls=200
                )
            )

            async for chunk in stream:
                if chunk.content:
                    content = chunk.content
                    
                    if isinstance(content, str):
                        text = content
                    elif hasattr(content, 'parts') and content.parts:
                        text_parts = []
                        for part in content.parts:
                            if hasattr(part, 'text') and part.text:
                                text_parts.append(part.text)
                        text = ''.join(text_parts)
                    else:
                        continue
                    
                    if text:
                        yield f'data: {json.dumps({"type": "text-delta", "id": text_id, "delta": text})}\n\n'

            yield f'data: {json.dumps({"type": "text-end", "id": text_id})}\n\n'
            
            yield f'data: {json.dumps({"type": "finish-step"})}\n\n'
            
            yield f'data: {json.dumps({"type": "finish"})}\n\n'
            
            yield 'data: [DONE]\n\n'
                
        except Exception as e:
            print(f"ERROR in stream_chat: {e}")
            import traceback
            traceback.print_exc()
            yield f'e:{json.dumps({"error": str(e)})}\n'
            
    