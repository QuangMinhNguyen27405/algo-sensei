"""Agent factory functions for creating LeetCode analysis agents."""
import os
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk import Runner
from google.adk.tools.google_search_tool import google_search
from google.adk.code_executors import BuiltInCodeExecutor
from google.genai.types import GenerateContentConfig

from google.adk.sessions import InMemorySessionService
from app.config.settings import settings

def create_runner(agent: Agent, session_service: InMemorySessionService) -> Runner:
    """Factory function to create a Runner with required session service and agent.
    
    Args:
        agent: The agent to associate with this runner
        session_service: Shared session service
    """
    
    if settings.google_api_key:
        os.environ["GOOGLE_API_KEY"] = settings.google_api_key
    
    return Runner(
        app_name="algo_sensei",
        agent=agent,
        session_service=session_service
    )

search_agent = Agent(
    model='gemini-2.0-flash',
    name='SearchAgent',
    instruction="""
    You're a specialist in Google Search
    """,
    tools=[google_search],
)
coding_agent = Agent(
    model='gemini-2.0-flash',
    name='CodeAgent',
    instruction="""
    You're a specialist in Code Execution
    """,
    code_executor=BuiltInCodeExecutor(),
)
    
root_agent = Agent(
    name="leetcode_root_agent",
    model="gemini-2.0-flash",
    description="Root agent for LeetCode analysis tasks",
    tools=[AgentTool(agent=search_agent), AgentTool(agent=coding_agent)],
    generate_content_config=GenerateContentConfig(
        response_modalities=["TEXT"],
    ),
    instruction="""You are an AI assistant specialized in analyzing LeetCode problems and providing hints and complexity analysis.

    Problem Description:
    {problem_description?}

    Current Code ({language?}):
    {code?}

    Provide helpful hints, explain concepts, and guide the user toward solving the problem without giving away the complete solution immediately.""",
)