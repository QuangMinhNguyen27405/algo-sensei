from pydantic import BaseModel

class HintRequestSchema(BaseModel):
    user_id: str
    session_id: str
    problem_description: str
    language: str
    code: str
    
class CodeAnalysisRequestSchema(BaseModel):
    user_id: str
    session_id: str
    problem_description: str
    language: str
    code: str
    
class HintResponseSchema(BaseModel):
    hints: str
    
class CodeAnalysisResponseSchema(BaseModel):
    analysis: str
