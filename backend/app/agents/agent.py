"""Agent factory functions for creating LeetCode analysis agents."""
import os
from google.adk.agents import LlmAgent
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from app.config.settings import settings

def create_complexity_analyzer() -> LlmAgent:
    """Factory function to create a complexity analysis agent."""
    return LlmAgent(
        model='gemini-2.0-flash-exp',
        name='complexity_analyzer',
        description="Analyzes the time and space complexity of algorithms in LeetCode solutions.",
        instruction=(
            "You are an expert algorithm complexity analyzer for LeetCode problems. "
            "When given code and programming language:\n"
            "1. Analyze the time complexity (Big O notation)\n"
            "2. Analyze the space complexity (Big O notation)\n"
            "3. Explain why the code has this complexity\n"
            "4. Identify any bottlenecks or inefficient operations\n"
            "5. Suggest potential optimizations if applicable\n\n"
            "Provide clear, concise explanations suitable for learning."
        ),
    )

def create_hint_agent() -> LlmAgent:
    """Factory function to create a hint providing agent."""
    return LlmAgent(
        model='gemini-2.0-flash-exp',
        name='hint_provider',
        description="Provides helpful hints and problem-solving guidance for LeetCode problems.",
        instruction=(
            "You are a helpful coding mentor for LeetCode problems. "
            "When given a problem description and current code:\n"
            "1. Understand the problem requirements\n"
            "2. Analyze the current approach\n"
            "3. Provide hints without giving away the complete solution\n"
            "4. Suggest data structures or algorithms that might help\n"
            "5. Point out common pitfalls or edge cases to consider\n\n"
            "Guide the user to discover the solution themselves. Be encouraging and educational."
        ),
        
    )

def create_runner(agent: LlmAgent, session_service: InMemorySessionService) -> Runner:
    """Factory function to create a Runner with required session service and agent.
    
    Args:
        agent: The agent to associate with this runner
        session_service: Optional shared session service, creates new one if not provided
    """
    
    if settings.google_api_key:
        os.environ["GOOGLE_API_KEY"] = settings.google_api_key
    
    if session_service is None:
        session_service = InMemorySessionService()
    
    return Runner(
        app_name="algo_sensei",
        agent=agent,
        session_service=session_service
    )