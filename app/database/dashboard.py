from config.environment import database
from bson import objectid
from app.utils.database import utils_db_get_token
from app.schemas.dashboard import CoordinatorRequest
from app.utils.helpers import get_ist_time, get_ist_date

class DBAnalyticsOps:
    def __init__(self):
        self.db = database["Analytics"]
        self.dashboard = self.db["Dashboard"]

    async def db_create_analytics(self, admin_id: str) -> None:
        data = {
            "admin_id": admin_id, 
            "date": get_ist_date(),
            "total": 0,
            "checked": 0,
            "skipped": 0,
            "removed": 0,
            "canceled": 0,
            "activity": []
        }
        
        await self.dashboard.insert_one(data)

    async def db_inc_total(self, admin_id: str) -> None:

        result = await self.dashboard.update_one(
            {"admin_id":admin_id, "date": get_ist_date()},
            {"$inc":{"total":1}}
        )

        if result.matched_count == 0:
            await self.db_create_analytics(admin_id)
            result = await self.dashboard.update_one(
                {"admin_id":admin_id, "date": get_ist_date()},
                {"$inc":{"total":1}}
            )
    async def db_inc_checked(self, admin_id: str) -> None:
            # implement a verification such that the total checked user dosen't exceeds the total number of users.

            result = await self.dashboard.update_one(
                {"admin_id":admin_id, "date": get_ist_date()},
                {"$inc":{"checked":1}}
            )
    
            if result.matched_count == 0:
                await self.db_create_analytics(admin_id)
                result = await self.dashboard.update_one(
                    {"admin_id":admin_id, "date": get_ist_date()},
                    {"$inc":{"total":1}}
                )
    async def db_inc_skipped(self, admin_id: str) -> None:
        result = await self.dashboard.update_one(
            {"admin_id":admin_id, "date": get_ist_date()},
            {"$inc":{"skipped":1}}
        )

        if result.matched_count == 0:
            await self.db_create_analytics(admin_id)
            await self.dashboard.update_one(
                {"admin_id":admin_id, "date": get_ist_date()},
                {"$inc":{"skipped":1}}
            )
    async def db_inc_cancel(self, admin_id: str):
        result = await self.dashboard.update_one(
            {"admin_id":admin_id, "date": get_ist_date()},
            {"$inc":{"canceled":1}}
        )

        if result.matched_count == 0:
            await self.db_create_analytics(admin_id)
            await self.dashboard.update_one(
                {"admin_id":admin_id, "date": get_ist_date()},
                {"$inc":{"canceled":1}}
            )

    async def db_inc_removed(self, admin_id: str) -> None:
        result = await self.dashboard.update_one(
            {"admin_id":admin_id, "date": get_ist_date()},
            {"$inc":{"removed":1}}
        )

        if result.matched_count() == 0:
            await self.db_create_analytics(admin_id)
            await self.dashboard.update_one(
                {"admin_id":admin_id, "date": get_ist_date()},
                {"$inc":{"removed":1}}
            )

    async def db_add_activity(self, admin_id: str, activity: str, info: str) -> None:
        data = {
            "type": activity,
            "info": info
        }

        await self.dashboard.update_one({"admin_id":admin_id, "date": get_ist_date()},
                                        {"$push": {"activity": data}})
        

analytics = DBAnalyticsOps()


# async def db_create_analytics(admin_id:str):
#     data = {
#         "admin_id":admin_id,
#         "total":0,
#         "skipped":0,
#         "checked":0,
#         "removed":0,
#         "canceled":0
#     }
#     db = database["Analytics"]
#     dashboard = db["Dashboard"]

#     await dashboard.insert_one(data)

async def db_get_dashboard_stats(admin_id) -> dict:
    '''
    Note: Dashboard analytics are updated for selection as per the date, so you can update it for:
        -> Last 7 days activity
        -> Selected date activity
        -> etc..
    '''
    try:
        db = database["Analytics"]
        dashboard = db["Dashboard"]

        result = await dashboard.find_one({"admin_id":admin_id, "date": get_ist_date()},{"_id":0})
        
        if result:
            data = {
                "total": result["total"],
                "checked": result["checked"],
                "waiting": result["total"] - (result["checked"] + result["canceled"]),
                "canceled": result["canceled"],
                "activity": result["activity"][::-1][:6]
            }
            return {
                "message":"Admin Dashboard data fetched!",
                "status":True,
                "data":data
            }
        else:
            data = {
                "total": 0,
                "checked": 0,
                "waiting": 0,
                "canceled": 0
            }
            return {
                "message":"Admin Dashboard data not found!",
                "status":True,
                "data":data
            }

    except Exception as e:
        return {
            "message":f"Admin Dashboard data can't be fetched:{e}",
            "status":False,
            "data":None
        }
    
async def db_get_recentActivity(admin_id: str) -> dict:
    db = database["Analytics"]
    dashboard = db["Dashboard"]
    result = await dashboard.find_one({"admin_id":admin_id, "date": get_ist_date()},{"_id":0})
    if result:
        data = {
            "status": True,
            "message": "Activity fetched successfully.",
            "data": result["activity"][::-1]
        }
    else:
        data = {
            "status": True,
            "message": "Activity fetched successfully.",
            "data": []
        }

    return data

async def db_show_coordinators(admin_email:str):
    try:
        db = database["Coordinators"]
        token = await utils_db_get_token(email=admin_email)

        collection = db[token]
        result = await collection.find({}).to_list(length=None)
        coordinators = result[0]["team"]

        return {
            "status":True,
            "message":"Coordinators Fetched!",
            "data":coordinators
        }

    except Exception as e:
        return {
            "status":False,
            "message":f"Can't fetch data due to:{e}",
            "data":{}
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

async def db_delete_coordinator(admin_email:str, coordinator_email:str):
    try:
        db = database["Coordinators"]
        token = await utils_db_get_token(email=admin_email)
        collection = db[token]

        result = await collection.find({}).to_list(length=None)
        coordinators:dict = result[0]["team"]

        if coordinator_email in list(coordinators.keys()):
            del coordinators[coordinator_email]
            await collection.update_one(
                {"email":admin_email},
                {"$set":{"team":coordinators}}
            )
            return {
                "message":"Coordinator Deleted Successfully!",
                "status":True
            }
        else:
            return {
                "message":"Coordinator not found!",
                "status":False
            }
    except Exception as e:
        return {
            "message":f"Deletion Failed:{e}",
            "status":False
        }

async def db_cancel_registration(client_id:str, form_id:str):
    try:
        db = database["Submissions"]
        collection = db[form_id]
        await collection.update_one(
            {"client_id":client_id},
            {"$set":{"cancelled":True, "checked_time":get_ist_time()}}
        )
        return {
            "message":"Registration cancelled successfully",
            "status":True
        }
    except Exception as e:
        return {
            "message":f"Operation Failed due to:{e}",
            "status":False
        }

async def db_done_missed(client_id:str, form_id:str):
    try:
        db = database["Submissions"]
        collection = db[form_id]
        await collection.update_one(
            {"client_id":client_id},
            {"$set":{"missed":True}}
        )
        return {
            "message":"Registration marked as missed successfully",
            "status":True
        }
    except Exception as e:
        return {
            "message":f"Operation Failed due to:{e}",
            "status":False
        }

# async def db_update_analytics(admin_id:str, field:str):
#     try:
#         db = database["Analytics"]
#         dashboard = db["Dashboard"]
        
#         await dashboard.update_one(
#             {"admin_id":admin_id},
#             {"$inc":{field:1}}
#         )
#         return {
#             "message":"Analytics updated successfully",
#             "status":True
#         }
#     except Exception as e:
#         print(e)
#         return {
#             "message":f"Action was successful but dashboard update failed due to:{e}",
#             "status":False
#         }