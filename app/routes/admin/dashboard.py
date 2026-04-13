from fastapi import APIRouter, status, HTTPException, Depends

from app.database.dashboard import db_get_dashboard_stats, db_add_coordinator
from app.schemas.dashboard import DashboardResponse, CoordinatorRequest, CoordinatorResponse
from app.schemas.errors import ErrorResponse

from app.utils.security import verify_request
router = APIRouter(prefix="/api/admin/dashboard", tags=["Admin Dashboard"])


@router.get("/",
            response_model=DashboardResponse,
            responses={code: {"model":ErrorResponse} for code in [401]}
            )
async def dashboard(info:str = Depends(verify_request)):
    try:
        admin_id = info["sub"]["id"]
        dashboard_data = await db_get_dashboard_stats(admin_id)
        if dashboard_data["status"]:
            return DashboardResponse(**dashboard_data)
        else:
            return DashboardResponse(
                status=False,
                message=dashboard_data["message"],
                data=None
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorResponse(
                message="Unable to load dashboard.",
                error=f"ERROR FOUND:{e}",
                success=False
            ).model_dump()
        )
    
@router.post("/add-cordinator",
             response_model=CoordinatorResponse,
             responses={code:{"model":ErrorResponse} for code in [500]})
async def add_cordinator(data:CoordinatorRequest, info:str):#= Depends(verify_request)
    try:
        admin_email = info #["sub"]["email"]
        result = await db_add_coordinator(admin_email=admin_email, coordinator=data)
        return CoordinatorResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                message="Operation Failed!",
                error=f"Information:{e}",
                success=False
            )
        )
