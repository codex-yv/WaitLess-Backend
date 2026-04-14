from fastapi import APIRouter, HTTPException, status, Depends

from app.database.forms import db_get_forms, db_create_form

from app.schemas.errors import ErrorResponse
from app.schemas.forms import FormsResponse, CreateFormRequest, CreateFormResponse

from app.utils.security import verify_request
router = APIRouter(prefix="/api/admin/form", tags=["Admin Form"])


# api to get all the available forms

@router.get("/",
            response_model=FormsResponse,
            responses={code:{"model":ErrorResponse} for code in [500, 401]})
async def get_forms(jwt_info:str = Depends(verify_request)):
    try:
        admin_email = jwt_info["sub"]["email"]
        result = await db_get_forms(admin_email=admin_email)
        
        return FormsResponse(**result)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                message="Failed to get forms!",
                error=f"Faliure due to:{e}",
                success=False
            ).model_dump()
        )

# api to create new form

@router.post("/create-form",
             response_model = CreateFormResponse,
             responses = {code:{"model":ErrorResponse} for code in [500, 401]})
async def create_form(data:CreateFormRequest, jwt_info:str = Depends(verify_request)):
    try:
        admin_email = jwt_info["sub"]["email"]
        result = await db_create_form(admin_email=admin_email, form_params=data)
        return CreateFormResponse(**result)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                message="Failed to create forms!",
                error=f"Faliure due to:{e}",
                success=False
            ).model_dump()
        )
    