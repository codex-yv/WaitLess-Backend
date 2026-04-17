from fastapi import APIRouter, Request, HTTPException, status, Response
from app.database.auth import db_valid_user, db_create_user, db_verify_coordinator, db_google_login, db_google_verify
from app.schemas.auth import LoginRequest, LoginResponse, SignupRequest, SignupResponse, CoordinatorLoginRequest, CoordinatorLoginResponse
from app.schemas.errors import ErrorResponse

from app.utils.security import create_access_token
from config.deployment import SECURE, SITES
from config.environment import GOOGLE_CLIENT_ID

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from pydantic import BaseModel

class GoogleTokenRequest(BaseModel):
    token: str

router = APIRouter(prefix="/api/auth", tags=["Login and Sign up"])


@router.post("/login",
             response_model = LoginResponse,
             responses = {code: {"model":ErrorResponse} for code in [500]})
async def login(response:Response, data:LoginRequest):
    try:
        result = await db_valid_user(data)
        if result["status"]:
            access_token = create_access_token({"sub":data.email, "user_data":{"id":result["id"], "email":data.email, "admin":True}})
            return LoginResponse(
                message=result["message"],
                status=result["status"],
                admin_id=result["id"],
                access_token=access_token,
                token_type="bearer"
            )
        else:
            return LoginResponse(
                message=result["message"],
                status=result["status"],
                admin_id=None,
                access_token=None,
                token_type=None
            )
    except Exception as e:
        print(e)
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
            access_token = create_access_token({"sub":data.email, "user_data":{"id":result["id"], "email":data.email, "admin":True}})
            return SignupResponse(
                message=result["message"],
                status=result["status"],
                admin_id=result["id"],
                access_token=access_token,
                token_type="bearer"
            )
        else:
            return SignupResponse(
                message=result["message"],
                status=result["status"],
                admin_id=None,
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
    

@router.post("/login/coordinator",
             response_model=CoordinatorLoginResponse,
             responses={code:{"model":ErrorResponse} for code in [500]})
async def coordinator_login(data:CoordinatorLoginRequest):
    try:
        result = await db_verify_coordinator(data)
        if result["status"]:
            access_token = create_access_token({"sub":result["admin_email"], "user_data":{"email":result["admin_email"],"id":result["admin_id"], "admin":False}})
            return CoordinatorLoginResponse(
                message=result["message"],
                status=result["status"],
                access_token=access_token,
                token_type="bearer"
            )
        else:
            return CoordinatorLoginResponse(
                message=result["message"],
                status=result["status"],
                access_token=None,
                token_type=None
            )
      
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                message="Login Failed!",
                error=f"Login Failed:{e}",
                success=False
            )
        )

import requests

class GoogleVerifyResponse(BaseModel):
    message: str
    status: bool
    exists: bool
    email: str | None = None
    name: str | None = None

@router.post("/google/login", response_model=LoginResponse)
async def google_login_route(data: GoogleTokenRequest):
    try:
        # Verify the Google Token (access_token)
        response = requests.get('https://www.googleapis.com/oauth2/v3/userinfo', headers={'Authorization': f'Bearer {data.token}'})
        
        if not response.ok:
            raise ValueError("Invalid Token")

        id_info = response.json()
        email = id_info.get("email")
        
        # Look up user in Database
        result = await db_google_login(email)
        
        if result["status"]:
            # Setup JWT Token
            access_token = create_access_token(
                {"sub": email, "user_data": {"id": result["id"], "email": email, "admin": True}}
            )
            return LoginResponse(
                message=result["message"],
                status=True,
                admin_id=result["id"],
                access_token=access_token,
                token_type="bearer"
            )
        else:
             return LoginResponse(
                 message=result["message"], 
                 status=False,
                 admin_id=None,
                 access_token=None,
                 token_type=None
            )
             
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid Google token")

@router.post("/google/verify", response_model=GoogleVerifyResponse)
async def google_verify_route(data: GoogleTokenRequest):
    try:
        response = requests.get('https://www.googleapis.com/oauth2/v3/userinfo', headers={'Authorization': f'Bearer {data.token}'})
        if not response.ok:
            raise ValueError("Invalid Token")

        id_info = response.json()
        email = id_info.get("email")
        name = id_info.get("name")
        
        # Check if email exists
        result = await db_google_verify(email, name)
        return GoogleVerifyResponse(
            message=result["message"],
            status=result["status"],
            exists=result["exists"],
            email=result.get("email"),
            name=result.get("name")
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid Google token")