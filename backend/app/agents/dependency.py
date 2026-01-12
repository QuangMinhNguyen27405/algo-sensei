"""Dependency injection for agent services."""
from google.adk.sessions import InMemorySessionService

from app.agents.agent import create_complexity_analyzer, create_hint_agent, create_runner
from app.agents.service import AgentService

_session_service = InMemorySessionService()

def get_agent_dependencies():
    """
    Create and cache agent dependencies (singleton pattern).
    
    The runner is initialized with an agent and shares the same session service.
    
    Returns:
        Tuple of (runner, complexity_analyzer, hint_agent, session_service)
    """
    complexity_analyzer = create_complexity_analyzer()
    hint_agent = create_hint_agent()
    
    runner = create_runner(agent=complexity_analyzer, session_service=_session_service)
    
    return runner, complexity_analyzer, hint_agent, _session_service


def get_agent_service() -> AgentService:
    """
    Dependency to get AgentService instance.
    
    Returns:
        AgentService: Configured agent service with all dependencies
    """
    runner, complexity_analyzer, hint_agent, session_service = get_agent_dependencies()
    return AgentService(
        runner=runner,
        complexity_analyzer=complexity_analyzer,
        hint_agent=hint_agent,
        session_service=session_service
    )
