"""Dependency injection for agent services."""
from google.adk.sessions import InMemorySessionService
from app.agents.agent import create_runner, root_agent
from app.agents.service import AgentService

_session_service = InMemorySessionService()

def get_agent_dependencies():
    """
    Create and cache agent dependencies (singleton pattern).
    
    The runner is initialized with an agent and shares the same session service.
    
    Returns:
        Tuple of (runner, session_service)
    """
    
    runner = create_runner(agent=root_agent, session_service=_session_service)
    
    return runner, _session_service


def get_agent_service() -> AgentService:
    """
    Dependency to get AgentService instance.
    
    Returns:
        AgentService: Configured agent service with all dependencies
    """
    runner, session_service = get_agent_dependencies()
    return AgentService(
        runner=runner,
        session_service=session_service
    )
