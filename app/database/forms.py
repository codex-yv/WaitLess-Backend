from bson import ObjectId
from config.environment import database
from app.schemas.forms import CreateFormRequest,SubmitFormRequest 
from app.utils.helpers import get_ist_date, is_time_expired, get_ist_time

async def db_get_forms(admin_id:str):
    try:
        db = database["Forms"]
        collection = db["forms"]

        query = {"admin_id": admin_id}
        forms = await collection.find(query).to_list(length=None)
        results = []
        if forms:
            for document in forms:
                document["_id"] = str(document["_id"])  # convert ObjectId to string if needed
                document["expired"] = is_time_expired(document["closes"], document["date"])
                results.append(document)
            # print(results[::-1])
            return {
                "message":"forms found!",
                "error":None,
                "data": results[::-1],
                "status":True
            }
        else:
            return {
                "message":"No forms available, please create some!",
                "error":None,
                "data": None,
                "status":True
            }
    except Exception as e:
        return {
            "message":"Failed to get forms from database.",
            "data":None,
            "error":f"Error Description:{e}",
            "status":False
        }
    

async def db_get_form_by_id(form_id:str):
    try:
        db = database["Forms"]
        collection = db["forms"]

        forms = await collection.find({"_id":ObjectId(form_id)}).to_list(length=None)
        if forms:
            await collection.update_one(
                {"_id":ObjectId(form_id)},
                {"$inc":{"total_scans":1}}
            )
            forms[0]["_id"] = str(forms[0]["_id"])
            # print(is_time_expired(forms[0]["closes"]))
            if not is_time_expired(forms[0]["closes"], forms[0]["date"]):
                return {
                    "message":"Form found!",
                    "data":forms,
                    "error":None,
                    "status":True
                }
            else:
                return {
                    "message":"Form has expired!",
                    "data":None,
                    "error":None,
                    "status":True
                }
        else:
            return {
                "message":"Invalid Scan!",
                "data":None,
                "error":None,
                "status":True
            }
        
    except Exception as e:
        return {
            "message":"Failed to get forms from database.",
            "data":None,
            "error":f"Error Description:{e}",
            "status":False
        }


async def db_create_form(admin_id:str, form_params:CreateFormRequest):
    try:
        db = database["Forms"]
        collection = db["forms"]

        forms_data = {
            "admin_id":admin_id,
            "forms_params":form_params.form_params,
            "title":form_params.title,
            "opens":form_params.opens_at,
            "closes":form_params.closes_at,
            "date": get_ist_date(),
            "started":False,
            "total_scans":0
        }
        
        result = await collection.insert_one(forms_data)
        return {
            "message":"Form created successfully!",
            "form_id":str(result.inserted_id),
            "error":None,
            "status":True
        }
    
    except Exception as e:
        return {
            "message":"Form not created!",
            "form_id":None,
            "error": f"Operation Unsuccessful:{e}",
            "status":False
        }
    
async def db_submit_client_form(data:SubmitFormRequest, client_id:str):
    try:
        db = database["Submissions"]
        collection = db[data.form_id]

        form_format = {
            "client_id":client_id,
            "params_val":data.params_val,
            "submitted_at":get_ist_time(),
            "serving": False,
            "checked":False,
            "checked_time":None,
            "skipped":False,
            "cancelled":False,
            "missed":False,
            "notifications":[]
        }

        await collection.insert_one(form_format)
        return {
            "message":"Form submitted successfully!",
            "error":None,
            "status":True
        }
    except Exception as e:
        return {
            "message":"Form not saved!",
            "form_id":None,
            "error": f"Operation Unsuccessful:{e}",
            "status":False
        }

async def db_get_all_submissions(form_id:str):
        db = database["Submissions"]
        collection = db[form_id]
        result = await collection.find({}).to_list(length=None)
        return result


# <----------- Remove the below function if not in use ------------->

async def db_get_current_stats(form_id:str, client_id:str):
    db = database["Submission"]
    collections = db[form_id]

    submissions = await collections.find({}).to_list(length=None)

    turn = 0
    position = 1
    for submission in submissions:
        if submission["checked"] or submission["skipped"]:
            turn +=1
    
    for submission in submissions:
        if not submission["cancelled"]:
            if submission["client_id"] != client_id:
                position+=1
            else:
                break

    return turn, position
