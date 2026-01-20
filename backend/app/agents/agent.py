"""Agent factory functions for creating LeetCode analysis agents."""
import os
import logging
from google.adk.agents import Agent
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from app.config.settings import settings

def create_runner(agent: Agent, session_service: InMemorySessionService) -> Runner:
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
    
root_agent = Agent(
    name="leetcode_root_agent",
    model="gemini-2.0-flash",
    description="Root agent for LeetCode analysis tasks",
    instruction="You are an AI assistant specialized in analyzing LeetCode problems and providing hints and complexity analysis.",
)