from fastapi import APIRouter, Depends, HTTPException
from app.utils.security import verify_request
from app.utils.positioning import get_current_stats, QUEUE
from app.database.dashboard import db_cancel_registration, db_done_missed, analytics
from app.utils.database import utils_db_get_admin_id_from_form_id

from communication.RTC import rtc
router = APIRouter(prefix="/api/client/dashboard", tags=["Client Dashboard"])

@router.get("/")
async def get_client_dashboard(jwt_data:dict = Depends(verify_request)):
    client_id = jwt_data["client_id"]
    form_id = jwt_data["form_id"]
    # print("Client ID:", client_id)
    # print("Form ID:", form_id)
    try:
        data = QUEUE.getQueueStats(form_id = form_id, client_id = client_id)
        # ys, cp, et, notify, temp, skipped, cancelled = await get_current_stats(client_id=client_id, form_id=form_id)
        # # if the returned values are 0 then show some specific message
        return {
            "message": "You have already registered!",
            "status": True,
            # "template": temp,
            "your_spot": data["current_pos"],
            "current_pos": data["current_turn"],
            # "extpected_time": et,
            # "noification": notify,
            "skipped": data["skipped"],
            "cancelled": data["current_pos"] and data["current_turn"],
        }
        # print(data)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error Due to:{e}"
        )

@router.post("/cancel")
async def cancel_registration(jwt_data:dict = Depends(verify_request)):
    client_id = jwt_data["client_id"]
    form_id = jwt_data["form_id"]
    try:
        result = await db_cancel_registration(client_id=client_id, form_id=form_id)
        admin_id = await utils_db_get_admin_id_from_form_id(form_id)
        if admin_id:
            await analytics.db_inc_cancel(admin_id = admin_id)

        await QUEUE.cancelRegistration(form_id = form_id, client_id = client_id)
        # Real-time updates: update admin's live queue & dashboard + all waiting clients' positions
        await rtc.submitCancelAppointment(admin_id=admin_id, client_id=client_id, form_id=form_id)
        await rtc.broadcastQueueUpdate(form_id=form_id)

        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error Due to:{e}"
        )

@router.post("/done-missed")
async def done_missed(jwt_data:dict = Depends(verify_request)):
    client_id = jwt_data["client_id"]
    form_id = jwt_data["form_id"]
    try:
        result = await db_done_missed(client_id=client_id, form_id=form_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error Due to:{e}"
        )
