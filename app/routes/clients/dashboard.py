from fastapi import APIRouter, Depends, HTTPException
from app.utils.security import verify_request
from app.utils.positioning import get_current_stats

router = APIRouter(prefix="/api/client/dashboard", tags=["Client Dashboard"])

@router.get("/")
async def get_client_dashboard(jwt_data:dict = Depends(verify_request)):
    client_id = jwt_data["client_id"]
    form_id = jwt_data["form_id"]

    try:
        ys, cp, et, notify, temp = await get_current_stats(client_id=client_id, form_id=form_id)
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