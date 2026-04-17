from config.environment import database
from bson import ObjectId

async def utils_db_get_token(email:str) -> str:
    db = database["Admins"]
    admin = db[email]

    result = await admin.find_one({"email":email})
    return result["token"]

async def utils_db_create_coordinators(token:str, email, admin_id):
    db = database["Coordinators"]
    collection = db[token]

    data = {
        "admin_id":admin_id,
        "email":email,
        "team":{}
    }

    await collection.insert_one(data)

async def utils_db_get_form_activated(form_id: str):
    db = database["Forms"]
    collection = db["forms"]

    form = await collection.find_one({"_id": ObjectId(form_id)})
    return form["started"]

async def utils_db_update_form_activated(form_id:str):
    db = database["Forms"]
    collection = db["forms"]

    await collection.update_one({"_id": ObjectId(form_id)}, {"$set": {"started": True}})

async def utils_db_get_admin_id_from_form_id(form_id:str):
    try:
        db = database["Forms"]
        collection = db["forms"]

        result = await collection.find_one({"_id": ObjectId(form_id)})
        return result["admin_id"]
    except Exception as e:
        print("Error in utils_db_get_admin_id_from_form_id:")
        print(e)
        return None