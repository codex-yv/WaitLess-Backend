from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.security import verify_request, create_admin_token, create_access_token
from app.utils.positioning import get_current_stats
from app.database.forms import db_get_form_by_id, db_submit_client_form
from app.schemas.forms import FormsResponse, SubmitFormRequest, SubmitFormResponse
from app.schemas.errors import ErrorResponse
from typing import Union

router = APIRouter(prefix="/api/forms", tags=["Client forms"])

# api to get form when user scans a QR

@router.get("/new",
            response_model=FormsResponse,
            responses = {code:{"model":ErrorResponse} for code in [500, 401]})
async def get_scanned_form(form_id:str):
    try:
        result = await db_get_form_by_id(form_id)
        return FormsResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                message="Failed to get form params.",
                error=f"Failed due to:{e}",
                success = False
            ).model_dump()
        )

@router.get("/exist")
async def get_scanned_form2(jwt_data:dict = Depends(verify_request)):
    try:
        ys, cp, et, notify, temp = await get_current_stats(client_id=jwt_data["client_id"], form_id=jwt_data["form_id"])
        # if the returned values are 0 then show some specific message
        return {
            "message":"You have already registered!",
            "status":True,
            "template":temp,
            "your_spot":ys,
            "current_pos":cp,
            "expected_time":et,
            "notification":notify
            }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error Due to:{e}"
        )
        

@router.post("/submit",
             response_model=SubmitFormResponse,
             responses={code:{"model":ErrorResponse} for code in [500]})
async def submit_client_form(data:SubmitFormRequest):
    try:
        client_id = create_admin_token() # using admin token to create clien token
        result = await db_submit_client_form(data=data, client_id=client_id)
        if result["status"]:
            jwt_data = {"user_data":{"client_id":client_id, "form_id":data.form_id}}
            access_token = create_access_token(data=jwt_data)
            return SubmitFormResponse(
                message=result["message"],
                error=result["error"],
                status=result["status"],
                access_token=access_token,
                token_type="bearer"
            )
        else:
            return SubmitFormResponse(
                message=result["message"],
                error=result["error"],
                status=result["status"],
                access_token=None,
                token_type=None
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                message="Error occurred during form submission.",
                error=f"Error due to:{e}",
                success=False
            ).model_dump()
        )