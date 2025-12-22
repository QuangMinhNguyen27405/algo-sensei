from fastapi import HTTPException

class BadRequestException(HTTPException):
    def __init__(self, detail: str = "Bad Request"):
        super().__init__(status_code=400, detail=detail)

class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(status_code=401, detail=detail)
        
class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Not Found"):
        super().__init__(status_code=404, detail=detail)
        
class AlreadyExistsException(HTTPException):
    def __init__(self, detail: str = "Resource Already Exists"):
        super().__init__(status_code=409, detail=detail)