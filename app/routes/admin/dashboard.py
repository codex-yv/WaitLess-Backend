from fastapi import APIRouter, status, HTTPException, Depends

from app.database.dashboard import db_get_dashboard_stats, db_add_coordinator, db_show_coordinators, db_delete_coordinator, db_get_recentActivity
from app.schemas.dashboard import (DashboardResponse, CoordinatorRequest, CoordinatorResponse, ShowCoordinatorResponse, 
                                   DeleteCoordinatorRequest, DeleteCoordinatorResponse, DashboardActivityResponse)
from app.schemas.errors import ErrorResponse

from app.utils.security import verify_request
router = APIRouter(prefix="/api/admin/dashboard", tags=["Admin Dashboard"])


@router.get("/",
            response_model=DashboardResponse,
            responses={code: {"model":ErrorResponse} for code in [401]}
            )
async def dashboard(info:dict = Depends(verify_request)):
    try:
        admin_id = info["id"]
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
    
@router.get("/activity",
            response_model = DashboardActivityResponse,
            responses = {code:{"model": ErrorResponse} for code in [500, 401]})
async def get_recent_activity(jwt_info: dict = Depends(verify_request)):
    try:
        result = await db_get_recentActivity(admin_id = jwt_info["id"])
        return DashboardActivityResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                message="Unable to load recent activity.",
                error=f"ERROR FOUND:{e}",
                success=False
            ).model_dump()
        )


@router.get("/show-coordinators",
            response_model=ShowCoordinatorResponse,
            responses = {code:{"model":ErrorResponse} for code in [500, 401]})
async def show_coordinators(info:dict = Depends(verify_request)):
    try:
        admin_email = info["email"]
        result = await db_show_coordinators(admin_email=admin_email)
        return ShowCoordinatorResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                message="Operation Failed!",
                error=f"Information:{e}",
                success=False
            ).model_dump()
        )




@router.post("/add-coordinator",
             response_model=CoordinatorResponse,
             responses={code:{"model":ErrorResponse} for code in [500]})
async def add_cordinator(data:CoordinatorRequest, info:dict= Depends(verify_request)):
    try:
        admin_email = info["email"]
        result = await db_add_coordinator(admin_email=admin_email, coordinator=data)
        return CoordinatorResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                message="Operation Failed!",
                error=f"Information:{e}",
                success=False
            ).model_dump()
        )

@router.post("/delete-coordinator",
             response_model=DeleteCoordinatorResponse,
             responses = {code:{"model":ErrorResponse} for code in [500, 401]})
async def delete_coordinator(data:DeleteCoordinatorRequest, info:dict = Depends(verify_request)):
    try:
        admin_email = info["email"]
        result = await db_delete_coordinator(admin_email=admin_email, coordinator_email= data.email)
        return DeleteCoordinatorResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                message="Operation Failed!",
                error=f"Information:{e}",
                success=False
            ).model_dump()
        )