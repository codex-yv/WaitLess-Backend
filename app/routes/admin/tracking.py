from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.security import verify_request
from app.schemas.tracking import LiveTrackingResponse, NextCustomerRequest, NextCustomerResponse
from app.schemas.errors import ErrorResponse

from app.database.tracking import db_get_live_tracking, db_next_customer, db_skip_customer, db_cancel_customer
from app.database.dashboard import analytics
from app.utils.positioning import QUEUE
from communication.RTC import rtc

router = APIRouter(prefix="/api/admin/tracking", tags=["Tracking"])


@router.get("/live",
            response_model=LiveTrackingResponse,
            responses={code:{"model":ErrorResponse} for code in [500, 401]})
async def get_live_tracking(form_id: str, jwt_data:dict = Depends(verify_request)):
    try:
        result = await db_get_live_tracking(form_id=form_id)
        return LiveTrackingResponse(**result)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                message="Failed to get live tracking!",
                error=f"Faliure due to:{e}",
                success=False
            ).model_dump()
        )


@router.post("/next",
            response_model=NextCustomerResponse,
            responses={code:{"model":ErrorResponse} for code in [500, 401]})
async def next_customer(data: NextCustomerRequest, jwt_data:dict = Depends(verify_request)):
    try:
        admin_id = jwt_data["id"]
        result = await db_next_customer(form_id=data.form_id, client_id=data.client_id)

        await analytics.db_inc_checked(admin_id)

        result["message"] = "Successful"

        await QUEUE.callNext(form_id = data.form_id )
        
        # Real-time updates: update all waiting clients' positions + admin's live queue & dashboard
        await rtc.broadcastQueueUpdate(form_id=data.form_id)
        await rtc.submitFormToAdmin(admin_id=admin_id, form_id=data.form_id, data=[])
        

        return NextCustomerResponse(**result)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                message="Failed to get next customer!",
                error=f"Faliure due to:{e}",
                success=False
            ).model_dump()
        )

@router.post("/skip",
            response_model=NextCustomerResponse,
            responses={code:{"model":ErrorResponse} for code in [500, 401]})
async def skip_customer(data: NextCustomerRequest, jwt_data:dict = Depends(verify_request)):
    try:
        result = await db_skip_customer(form_id=data.form_id, client_id=data.client_id)

        await analytics.db_inc_skipped(admin_id = jwt_data['id'])

        result["message"] = "Successful"

        await QUEUE.skipNext(client_id = data.client_id, form_id = data.form_id)

        # Real-time updates: notify skipped client + update all waiting clients' positions + admin
        await rtc.sendSkipByAdmin(client_id=data.client_id)
        await rtc.broadcastQueueUpdate(form_id=data.form_id)
        await rtc.submitFormToAdmin(admin_id=jwt_data["id"], form_id=data.form_id, data=[])
        

        return NextCustomerResponse(**result)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                message="Failed to skip customer!",
                error=f"Faliure due to:{e}",
                success=False
            ).model_dump()
        )

@router.post("/cancel",
            response_model=NextCustomerResponse,
            responses={code:{"model":ErrorResponse} for code in [500, 401]})
async def cancel_customer(data: NextCustomerRequest, jwt_data:dict = Depends(verify_request)):
    try:
        result = await db_cancel_customer(form_id=data.form_id, client_id=data.client_id)

        await analytics.db_inc_cancel(admin_id = jwt_data["id"])
        result["message"] = "Successful" # remove this params from schema and update frontend accordingly

        await QUEUE.cancelRegistration(form_id = data.form_id, client_id = data.client_id)
        
        # Real-time updates: notify cancelled client + update all waiting clients' positions + admin
        await rtc.sendCancelbyAdmin(client_id=data.client_id)
        await rtc.broadcastQueueUpdate(form_id=data.form_id)
        await rtc.submitFormToAdmin(admin_id=jwt_data["id"], form_id=data.form_id, data=[])

        return NextCustomerResponse(**result)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                message="Failed to cancel customer!",
                error=f"Faliure due to:{e}",
                success=False
            ).model_dump()
        )