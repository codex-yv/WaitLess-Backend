from fastapi import APIRouter, Request, HTTPException, status, Response
from app.database.auth import db_valid_user, db_create_user
from app.schemas.auth import LoginRequest, LoginResponse, SignupRequest, SignupResponse
from app.schemas.errors import ErrorResponse

from app.utils.security import create_access_token
from config.deployment import SECURE, SITES

router = APIRouter(prefix="/api/auth", tags=["Login and Sign up"])


@router.post("/login",
             response_model = LoginResponse,
             responses = {code: {"model":ErrorResponse} for code in [500]})
async def login(response:Response, data:LoginRequest):
    try:
        result = await db_valid_user(data)
        if result["status"]:
            access_token = create_access_token({"sub":{"id":result["id"], "email":data.email}})
            return LoginResponse(
                message=result["message"],
                status=result["status"],
                access_token=access_token,
                token_type="bearer"
            )
        else:
            return LoginResponse(
                message=result["message"],
                status=result["status"],
                access_token=None,
                token_type=None
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                success=False,
                error="Internal Server Error",
                message=f"Unable to login:{e}"
            ).model_dump(),
        )

@router.post("/signup",
             response_model = SignupResponse,
             responses = {code: {"model":ErrorResponse} for code in [500]})
async def signup(response:Response, data:SignupRequest):
    try:
        result = await db_create_user(data)
        if result["status"]:
            access_token = create_access_token({"sub":{"id":result["id"], "email":data.email}})
            return SignupResponse(
                message=result["message"],
                status=result["status"],
                access_token=access_token,
                token_type="bearer"
            )
        else:
            return SignupResponse(
                message=result["message"],
                status=result["status"],
                access_token=None,
                token_type=None
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                success=False,
                error="Internal Server Error",
                message=f"Unable to signup:{e}"
            ).model_dump(),
        )