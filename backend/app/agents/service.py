"""Service layer for agent-related operations."""
import json
from typing import List, Optional, AsyncGenerator
from google.adk.sessions import InMemorySessionService
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
        code: Optional[str] = None,
        language: Optional[str] = None,
        problem_description: Optional[str] = None
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
        
        # Get the last user message
        last_message = None
        for msg in reversed(messages):
            if msg.role == "user":
                last_message = self._extract_message_text(msg)
                break
        
        if not last_message:
            yield 'e:{"error":"No user message found"}\n'
            return
        
        context_parts = []
        
        if problem_description:
            context_parts.append(f"Problem Description:\n{problem_description}")
        
        if code and language:
            context_parts.append(f"Current code in {language}:\n```{language}\n{code}\n```")
        elif code:
            context_parts.append(f"Current code:\n```\n{code}\n```")
        
        context = "\n\n".join(context_parts) if context_parts else ""
        prompt = f"{context}\n\nUser: {last_message}" if context else last_message
        
        try:
            await self.session_service.create_session(
                app_name="algo_sensei",
                user_id=user_id,
                session_id=session_id
            )
        except Exception:
            # Session might already exist
            pass
        
        message_content = Content(
            parts=[Part(text=prompt)],
            role="user"
        )
        
        try:
            has_content = False
            print(f"Starting Google ADK runner for session: {session_id}")
            
            for event in self.runner.run(
                user_id=user_id,
                session_id=session_id,
                new_message=message_content
            ):
                print(f"Event received: {type(event)}, {event}")
                
                # Stream tokens immediately as they arrive
                if hasattr(event, 'content') and event.content:
                    content = event.content
                    print(f"Event has content: {type(content)}")
                    
                    if isinstance(content, str) and content:
                        has_content = True
                        # Stream immediately (AI SDK format: text deltas with 0: prefix)
                        chunk = f'0:{json.dumps(content)}\n'
                        print(f"Streaming chunk: {chunk.strip()}")
                        yield chunk
                    elif hasattr(content, 'parts') and content.parts:
                        for part in content.parts:
                            if hasattr(part, 'text') and part.text:
                                has_content = True
                                # Stream immediately
                                chunk = f'0:{json.dumps(part.text)}\n'
                                print(f"Streaming chunk: {chunk.strip()}")
                                yield chunk
            
            if not has_content:
                print("WARNING: No response text streamed from Google ADK!")
                yield 'e:{"error":"No response generated from AI"}\n'
                return
            
            # Send finish message
            yield 'd:{"finishReason":"stop"}\n'
            print("Streaming completed successfully")
                
        except Exception as e:
            print(f"ERROR in stream_chat: {e}")
            import traceback
            traceback.print_exc()
            yield f'e:{json.dumps({"error": str(e)})}\n'
            
    