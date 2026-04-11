from config.environment import database
from app.schemas.auth import LoginRequest, SignupRequest, CoordinatorLoginRequest
from app.database.dashboard import db_create_analytics
from app.utils.database import utils_db_create_coordinators
from app.utils.security import create_admin_token


async def db_valid_user(data:LoginRequest)-> dict:
    try:
        db = database["Admins"]
        admins = await db.list_collection_names()

        if data.email in admins:
            admin = db[data.email]
            admin_data = await admin.find({},{"_id":1, "password":1}).to_list(None)
            print(admin_data)
            if admin_data[0]["password"] == data.password:
                return {
                    "message":"Login Successful",
                    "status":True,
                    "id":str(admin_data[0]["_id"]),
                }
            else:
                return {
                    "message":"Wrong password!",
                    "status":False,
                    "id":None,
                }
        else:
            return {
                "message":"Email does not exist!",
                "status":False,
                "id":None,
            }
    except Exception as e:
         return {
            "message":f"Unable to validate:{e}",
            "status":False,
            "id":None,
        }

async def db_create_user(data:SignupRequest)-> dict:
    try:
        db = database["Admins"]
        admins = await db.list_collection_names()

        if data.email in admins:
            return {
                "message":"Email already exists!",
                "status":False,
                "id":None,
            }
        else:
            admin = db[data.email]
            token = create_admin_token()
            admin_data = {
                "user_name":data.name,
                "email":data.email,
                "password":data.password,
                "occupation":data.occupation,
                "token":token
            }
            result = await admin.insert_one(admin_data)

            await db_create_analytics(str(result.inserted_id))
            await utils_db_create_coordinators(email = data.email, token=token)
            
            return {
                "message":"User created successfully!",
                "status":True,
                "id": str(result.inserted_id)
            }
    except Exception as e:
        return {
            "message":f"Unable to create:{e}",
            "status":False,
            "id":None,
        }
    

async def db_verify_coordinator(data:CoordinatorLoginRequest):
    try:
        db = database["Coordinators"]
        collections = await db.list_collection_names()
        if data.token in collections:
            collection = db[data.token]
            team = await collection.find_one({})
            if data.email in team["team"]:
                return {
                    "message":"Login Successful",
                    "status":True
                }
            else:
                return{
                    "message":"Email not found!",
                    "status":False
                }
        else:
            return {
                "message":"Invalid token.",
                "status":False
            }
    except Exception as e:
        return {
            "message": "Failed to verify credentials.",
            "Error": f"Details:{e}",
            "status":False,

        }