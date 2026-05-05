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
            admin_data = await admin.find({}).to_list(None)
            # print(admin_data)
            try:
                picture = admin_data[0]["profile_picture"]
            except KeyError:
                picture = None
            if admin_data[0]["password"] == data.password:
                return {
                    "message":"Login Successful",
                    "status":True,
                    "id":str(admin_data[0]["_id"]),
                    "email":data.email,
                    "profile_picture":picture
                }
            else:
                return {
                    "message":"Wrong password!",
                    "status":False,
                    "id":None,
                    "email":None,
                    "profile_picture":None
                }
        else:
            return {
                "message":"Email does not exist!",
                "status":False,
                "id":None,
                "email":None,
                "profile_picture":None
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
                "profile_picture":data.picture,
                "occupation":data.occupation,
                "org_type":data.org_type,
                "org_name":data.org_name,
                "address": data.address,
                "token":token
            }
            result = await admin.insert_one(admin_data)

            await db_create_analytics(str(result.inserted_id))
            await utils_db_create_coordinators(email = data.email, token=token, admin_id = str(result.inserted_id))
            
            return {
                "message":"User created successfully!",
                "status":True,
                "email":data.email,
                "picture":data.picture,
                "id": str(result.inserted_id)
            }
    except Exception as e:
        return {
            "message":f"Unable to create:{e}",
            "status":False,
            "email":None,
            "picture":None,
            "id":None,
        }
    

async def db_verify_coordinator(data:CoordinatorLoginRequest):
    try:
        db = database["Coordinators"]
        collections = await db.list_collection_names()
        if data.token in collections:
            collection = db[data.token]
            team_data = await collection.find_one({})
            team:dict = team_data["team"]
            if data.email in list(team.keys()):
                return {
                    "message":"Login Successful",
                    "admin_email":team_data["email"],
                    "admin_id":team_data["admin_id"],
                    "status":True
                }
            else:
                return{
                    "message":"Email not found!",
                    "admin_email":None,
                    "admin_id":None,
                    "status":False
                }
        else:
            return {
                "message":"Invalid token.",
                "admin_email":None,
                "admin_id":None,
                "status":False
            }
    except Exception as e:
        return {
            "message": "Failed to verify credentials.",
            "Error": f"Details:{e}",
            "status":False,

        }

async def db_google_login(email: str) -> dict:
    try:
        db = database["Admins"]
        admins = await db.list_collection_names()

        if email in admins:
            # User exists, login
            admin = db[email]
            admin_data = await admin.find({},{"_id":1}).to_list(None)
            return {
                "message": "Login Successful",
                "status": True,
                "id": str(admin_data[0]["_id"]),
            }
        else:
            return {
                "message": "Account does not exist! Please sign up first.",
                "status": False,
                "id": None
            }
    except Exception as e:
        return {
            "message": f"Unable to login: {e}",
            "status": False,
            "id": None,
        }

async def db_google_verify(email: str, name: str) -> dict:
    try:
        db = database["Admins"]
        admins = await db.list_collection_names()

        if email in admins:
            return {
                "message": "Email already exists!",
                "status": False,
                "exists": True,
                "email": email,
                "name": name
            }
        else:
            return {
                "message": "Google account verified. Please complete signup.",
                "status": True,
                "exists": False,
                "email": email,
                "name": name
            }
    except Exception as e:
        return {
            "message": f"Unable to verify: {e}",
            "status": False,
            "exists": False
        }