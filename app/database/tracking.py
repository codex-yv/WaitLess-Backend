from config.environment import database
from app.utils.helpers import get_ist_time, Previous, instance
from app.utils.database import utils_db_get_form_activated, utils_db_update_form_activated

async def db_get_live_tracking(form_id: str):
    try:
        db = database["Submissions"] 
        collections = db[form_id]

        submissions = await collections.find({}).to_list(length=None)
        result =[]
        for submission in submissions:
            submission["_id"] = str(submission["_id"])
            try:
                check = submission["serving"]
            except KeyError:
                submission["serving"] = False

            result.append(submission)
        started = await utils_db_get_form_activated(form_id)
        return {
            "message": "Live tracking data retrieved successfully",
            "status":True, 
            "started":started,
            "data":result
        }
    except Exception as e:
        return {
            "message": f"Failed to get live tracking data: {str(e)}",
            "status":False, 
            "started":False,
            "data":None
        }

async def db_next_customer(form_id: str, client_id: str):
    try:
        db = database["Submissions"] 
        collections = db[form_id]
        started = await utils_db_get_form_activated(form_id)
        await utils_db_update_form_activated(form_id)

        await collections.update_one(
            {"client_id": client_id},
            {"$set": {"checked": True, "checked_time": get_ist_time(), "serving":True}}
        )

        print("CLIENT_ID: ", client_id)

        obj = instance.getInstance(form_id)

        # checking if there is any instance for form_id
        if obj:
            # performing operations on the instance
            if obj.getPrevData():
                await collections.update_one(
                    {"client_id": obj.getPrevData()},
                    {"$set": {"serving":False}}
                )

            # adding the current client as previous
            obj.addPrevData(client_id)
        else:
            # creating instance if not exist.
            previous = Previous()
            previous.addPrevData(client_id)
            instance.addInstance(form_id, previous)

        return {
            "message": "Next customer updated successfully",
            "started": started,
            "status":True
        }
    except Exception as e:
        print(e)
        return {
            "message": f"Failed to update next customer: {str(e)}",
            "started": started,
            "status":False
        }


async def db_skip_customer(form_id: str, client_id: str):
    try:
        db = database["Submissions"] 
        collections = db[form_id]
        started = await utils_db_get_form_activated(form_id)
        await collections.update_one(
            {"client_id": client_id},
            {"$set": {"skipped": True, "checked_time": get_ist_time()}}
        )
        return {
            "message": "Skip customer updated successfully",
            "status":True,
            "started": started
        }
    except Exception as e:
        return {
            "message": f"Failed to update skip customer: {str(e)}",
            "status":False,
            "started": False
        }

async def db_cancel_customer(form_id: str, client_id: str):
    try:
        db = database["Submissions"] 
        collections = db[form_id]
        started = await utils_db_get_form_activated(form_id)
        
        await collections.update_one(
            {"client_id": client_id},
            {"$set": {"cancelled": True, "checked_time": get_ist_time()}}
        )
        return {
            "message": "Cancel customer updated successfully",
            "status":True,
            "started": started
        }
    except Exception as e:
        return {
            "message": f"Failed to update cancel customer: {str(e)}",
            "status":False,
            "started": False
        }