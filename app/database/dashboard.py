from config.environment import database
from bson import objectid
from app.utils.database import utils_db_get_token
from app.schemas.dashboard import CoordinatorRequest


async def db_create_analytics(admin_id:str):
    data = {
        "admin_id":admin_id,
        "total":0,
        "skipped":0,
        "removed":0,
        "canceled":0
    }
    db = database["Analytics"]
    dashboard = db["Dashboard"]

    await dashboard.insert_one(data)

async def db_get_dashboard_stats(admin_id) -> dict:
    try:
        db = database["Analytics"]
        dashboard = db["Dashboard"]

        result = await dashboard.find_one({"admin_id":admin_id},{"_id":0})
        if result:
            return {
                "message":"Admin Dashboard data not found!",
                "status":True,
                "data":result
            }
        else:
            return {
                "message":"Admin Dashboard data not found!",
                "status":False,
                "data":None
            }

    except Exception as e:
        return {
            "message":f"Admin Dashboard data can't be fetched:{e}",
            "status":False,
            "data":None
        }
    

async def db_add_coordinator(admin_email:str, coordinator:CoordinatorRequest):
    try:
        db = database["Coordinators"]
        token = await utils_db_get_token(admin_email)

        collection = db[token]
        coordinators = await collection.find_one({"email":admin_email})
        team:dict = coordinators["team"]

        if coordinator.email in list(team.keys()):
            return {
                "message":"Coordinator already exist.",
                "status":True
            }
        else:
            team[coordinator.email] = coordinator.name
            await collection.update_one(
                {"email":admin_email},
                {"$set":{"team":team}}
            )
            return {
                "message":"Coordinator added successfuly",
                "status":True
            }
    except Exception as e:
        return {
            "message":f"Operation Failed due to:{e}",
            "status":False
        }

