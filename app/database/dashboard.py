from config.environment import database

async def db_create_analytics():
    data = {
        "admin_id":"",
        "total":0,
        "skipped":0,
        "removed":0,
        "canceled":0
    }
    db = database["Analytics"]
    dashboard = db["Dashboard"]

    await dashboard.insert_one(data)