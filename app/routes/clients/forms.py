from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.security import verify_request, create_admin_token, create_access_token
# from app.utils.positioning import get_current_stats
from app.utils.database import utils_db_get_admin_id_from_form_id
from app.database.dashboard import db_update_analytics
from app.database.forms import db_get_form_by_id, db_submit_client_form
from app.schemas.forms import FormsResponse, SubmitFormRequest, SubmitFormResponse
from app.schemas.errors import ErrorResponse
from typing import Union

from communication.RTC import rtc

router = APIRouter(prefix="/api/forms", tags=["Client forms"])

# api to get form when user scans a QR

@router.get("/new",
            response_model=FormsResponse,
            responses = {code:{"model":ErrorResponse} for code in [500, 401]})
async def get_scanned_form(form_id:str):
    try:
        result = await db_get_form_by_id(form_id)
        admin_id = await utils_db_get_admin_id_from_form_id(form_id=form_id)
        if admin_id:
            await rtc.scanFormUpdate(admin_id=admin_id, form_id=form_id)
        print(result)
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
async def get_scanned_form2(client_id:str,form_id:str):#jwt_data:dict = Depends(verify_request)
    try:
        ...
        # ys, cp, et, notify, temp,skipped, cancelled = await get_current_stats(client_id=jwt_data["client_id"], form_id=jwt_data["form_id"])
        # if the returned values are 0 then show some specific message
        # return {
        #     "message":"You have already registered!",
        #     "status":True,
        #     "template":temp,
        #     "your_spot":ys,
        #     "current_pos":cp,
        #     "expected_time":et,
        #     "notification":notify
        #     }
    except Exception as e:
        print(e)
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
            admin_id = await utils_db_get_admin_id_from_form_id(data.form_id)
            if admin_id:
                # update analytics
                update_result = await db_update_analytics(admin_id = admin_id, field="total")
            
            await rtc.submitFormToAdmin(admin_id=admin_id, form_id=data.form_id, data=data.params_val) # added rtc
            
            return SubmitFormResponse(
                message=result["message"],
                error=result["error"],
                status=result["status"],
                client_id=client_id,
                access_token=access_token,
                token_type="bearer"
            )
        else:
            return SubmitFormResponse(
                message=result["message"],
                error=result["error"],
                status=result["status"],
                client_id=client_id,
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