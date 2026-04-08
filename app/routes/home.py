from fastapi import APIRouter, Request

router = APIRouter(prefix="/api/home", tags=["Home page"])



@router.get("/")
async def home(request:Request):
    logged_in = request.cookies.get("cred")
    if logged_in:
        return {
            "logged_in":True
        }
    return {
        "logged_in":False
    }