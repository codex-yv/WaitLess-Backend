from config.environment import database
from app.schemas.forms import CreateFormRequest


async def db_get_forms(admin_email:str):
    try:
        db = database["Forms"]
        collection = db[admin_email]

        forms = await collection.find_one({})
        if forms:
            forms["_id"] = str(forms["_id"])
            return {
                "message":"forms found!",
                "error":None,
                "data": forms,
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
    
async def db_create_form(admin_email:str, form_params:CreateFormRequest):
    try:
        db = database["Forms"]
        collection = db[admin_email]

        forms_data = {
            "forms_params":form_params.form_params,
            "opens":form_params.opens_at,
            "closes":form_params.closes_at
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
    
