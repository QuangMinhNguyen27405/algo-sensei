from fastapi import APIRouter, Depends

from app.agents.schemas import CodeAnalysisRequestSchema, HintRequestSchema, HintResponseSchema, CodeAnalysisResponseSchema
from app.agents.service import AgentService
from app.agents.dependency import get_agent_service

router = APIRouter(
    prefix="/agent",
    tags=["agent"]
)
    
@router.post("/get-hints", response_model=HintResponseSchema)
async def get_problem_hints(
    request: HintRequestSchema,
    agent_service: AgentService = Depends(get_agent_service)
):
    """
    Get hints and guidance for solving a LeetCode problem.
    Each tab should send its unique session_id to maintain conversation history.
    """
    hints = await agent_service.provide_hints(
        request.user_id,
        request.session_id,
        request.problem_description,
        request.code,
        request.language,
    )
    return HintResponseSchema(hints=hints)

@router.post("/analyze-complexity", response_model=CodeAnalysisResponseSchema)
async def analyze_code_complexity(
    request: CodeAnalysisRequestSchema,
    agent_service: AgentService = Depends(get_agent_service)
):
    """
    Analyze the time and space complexity of the provided code.
    Each tab should send its unique session_id to maintain conversation history.
    """
    analysis = await agent_service.analyze_complexity(
        request.user_id, 
        request.session_id, 
        request.problem_description, 
        request.language, 
        request.code
    )
    return CodeAnalysisResponseSchema(analysis=analysis)
