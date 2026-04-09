from fastapi import APIRouter, Request, Depends, HTTPException, status
from app.utils.security import verify_request
from app.schemas.errors import ErrorResponse
router = APIRouter(prefix="/api/home", tags=["Home page"])



@router.get("/", responses={code:{"model":ErrorResponse} for code in [401]})
async def home(request:Request, info:dict = Depends(verify_request)):
    try:
        return {
            "status":True
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorResponse(
                message="Unauthorized access",
                error=f"{e}",
                success=False
            )
        )