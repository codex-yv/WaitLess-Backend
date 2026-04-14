from config.environment import database

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
