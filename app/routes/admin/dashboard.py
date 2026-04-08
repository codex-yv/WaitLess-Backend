from fastapi import APIRouter

router = APIRouter(prefix="/api/admin/dashboard", tags=["Admin Dashboard"])


@router.get("/")
async def dashboard():
    email = ...
    return {
        "message":"Active Dashboard."
    }