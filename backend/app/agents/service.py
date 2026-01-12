"""Service layer for agent-related operations."""
import json
from google.adk.sessions import InMemorySessionService
from google.adk.agents.llm_agent import Agent
from google.adk import Runner
from google.genai.types import Content, Part


class AgentService:
    """Service for handling LeetCode analysis using AI agents."""
    
    def __init__(self, runner: Runner, complexity_analyzer: Agent, hint_agent: Agent, session_service: InMemorySessionService):
        """Initialize the AgentService with required dependencies.
        
        Args:
            runner: The Runner instance for executing agents
            complexity_analyzer: Agent for analyzing code complexity
            hint_agent: Agent for providing hints
            session_service: Shared session service for maintaining tab sessions
        """
        self.runner = runner
        self.complexity_analyzer = complexity_analyzer
        self.hint_agent = hint_agent
        self.session_service = session_service
        
    async def provide_hints(self, user_id: str, session_id: str, problem_description: str, code: str, language: str) -> str:
        """
        Provide hints and guidance for solving a LeetCode problem.
        
        Args:
            problem_description: The problem statement and requirements
            code: The user's current code attempt
            language: The programming language being used
            session_id: Unique session ID from the frontend tab (maintains conversation history)
            
        Returns:
            Hints and guidance without giving away the complete solution
        """
        user_session = user_id + "_" + session_id
        
        prompt = f"""
            The user is working on the following problem:

            {problem_description}

            Their current code in {language}:
            ```{language}
            {code}
            ```

            Provide helpful hints and guidance:
            1. Analyze their current approach
            2. Suggest data structures or algorithms that might help
            3. Point out common pitfalls or edge cases
            4. Give hints without revealing the complete solution
            5. Be encouraging and educational

            Remember to guide them to discover the solution themselves.
        """
        self.runner.agent = self.hint_agent
        
        # Create Content object from prompt
        message_content = Content(
            parts=[Part(text=prompt)],
            role="user"
        )
        
        result_text = ""
        
        # Create session if it doesn't exist
        try:
            await self.session_service.create_session(
                app_name="algo_sensei",
                user_id="leetcode_user",
                session_id=user_session
            )
        except Exception:
            # Throw exception if session already exists
            pass
        
        for event in self.runner.run(
            user_id="leetcode_user",
            session_id=user_session,
            new_message=message_content
        ):
            # Collect the final response text
            if hasattr(event, 'content') and event.content:
                if isinstance(event.content, str):
                    result_text = event.content
                elif hasattr(event.content, 'parts') and event.content.parts:
                    # Extract text from Content object
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            result_text += part.text
        
        return result_text or "No response generated"
    
    async def analyze_complexity(self, user_id: str, session_id: str, problem_description: str, code: str, language: str) -> str:
        """
        Analyze the time and space complexity of the given code.
        
        Args:
            code: The source code to analyze
            language: The programming language of the code
            session_id: Unique session ID from the frontend tab (maintains conversation history)
            
        Returns:
            Analysis result with time/space complexity and explanations
        """
        user_session = user_id + "_" + session_id
        
        prompt = f"""
            The user is working on the following problem:
            {problem_description}
            
            Analyze the following {language} code and provide:
            1. Time Complexity (Big O notation)
            2. Space Complexity (Big O notation)
            3. Detailed explanation of why the code has this complexity
            4. Any bottlenecks or inefficient operations
            5. Optimization suggestions if applicable

            Code:
            ```
            {code}
            ```
        """
        
        self.runner.agent = self.complexity_analyzer
        
        message_content = Content(
            parts=[Part(text=prompt)],
            role="user"
        )
        
        result_text = ""
        
        # Create session if it doesn't exist
        try:
            await self.session_service.create_session(
                app_name="algo_sensei",
                user_id="leetcode_user",
                session_id=user_session,
            )
        except Exception:
            # Throw exception if session already exists
            pass
        
        for event in self.runner.run(
            user_id="leetcode_user",
            session_id=user_session,
            new_message=message_content
        ):
            # Collect the final response text
            if hasattr(event, 'content') and event.content:
                if isinstance(event.content, str):
                    result_text = event.content
                elif hasattr(event.content, 'parts') and event.content.parts:
                    # Extract text from Content object
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            result_text += part.text
        
        return result_text or "No response generated"

