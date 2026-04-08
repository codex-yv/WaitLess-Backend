from config.environment import database
from app.schemas.auth import LoginRequest, SignupRequest
from app.database.dashboard import db_create_analytics

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
            admin_data = {
                "user_name":data.name,
                "email":data.password,
                "password":data.password,
                "occupation":data.occupation
            }
            result = await admin.insert_one(admin_data)
            await db_create_analytics()
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