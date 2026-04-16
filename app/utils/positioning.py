from app.database.forms import db_get_all_submissions
from datetime import datetime

async def get_current_stats(client_id:str, form_id:str):
    result = await db_get_all_submissions(form_id)
    if result:
        your_spot = 1
        current_pos = 0
        timing = []
        notification = []
        template = []
        for client in result:
            if (client["client_id"] != client_id):#and (not client["cancelled"] and not client["skipped"] and client["checked"]):
                your_spot+=1
                continue
            template = client["params_val"]
            break

        for client in result:
            if client["checked"] or client["skipped"]:
                current_pos+=1
                timing.append(client["checked_time"])
            if client["cancelled"]:
                your_spot-=1

            if client["client_id"] == client_id:
                notification = client["notifications"]

        n = len(timing)
        expected_time = 0
        if n>1:
            time_diff = []
            for time in range(0, n-1):
                fmt = "%H:%M:%S"
    
                time1 = datetime.strptime(timing[time], fmt)
                time2 = datetime.strptime(timing[time+1], fmt)
                
                diff = time2 - time1
                time_diff.append(diff.total_seconds() // 60)

            avg_time = sum(time_diff)//len(time_diff)    

            expected_time = avg_time * your_spot
        
        return your_spot, current_pos, expected_time, notification, template

    else:
        return 0, 0, 0, []