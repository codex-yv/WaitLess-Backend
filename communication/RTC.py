from fastapi import WebSocket, WebSocketDisconnect
from app.database.tracking import db_get_live_tracking
from app.database.dashboard import db_get_dashboard_stats
from app.database.forms import db_get_all_submissions
from app.utils.positioning import QUEUE
from datetime import datetime

class ConnectionManager:
    def __init__(self):
        self.connection:dict[str, WebSocket] = {}
    
    async def connect(self, req_id:str, websocket:WebSocket):
        await websocket.accept()
        self.connection[req_id] = websocket
    
    async def disconnect(self, req_id):
        del self.connection[req_id]

    async def scanFormUpdate(self, admin_id:str, form_id:str):
        if admin_id in self.connection:
            formatted_data = {
                "loc":"generate_form",
                "form_id":form_id,
            }
            await self.connection[admin_id].send_json(formatted_data)
    
    async def sendCancelbyAdmin(self, client_id:str):
        if client_id in self.connection:
            formatted_data = {
                "loc":"client_dash_cancel"
            }
            await self.connection[client_id].send_json(data=formatted_data)

    async def sendSkipByAdmin(self, client_id:str):
        if client_id in self.connection:
            formatted_data = {
                "loc":"client_dash_skip"
            }
            await self.connection[client_id].send_json(data=formatted_data)

    async def submitCancelAppointment(self, admin_id:str, client_id:str, form_id:str):
        if admin_id in self.connection:
            result_live_queue = await db_get_live_tracking(form_id=form_id)
            result_dashboard = await db_get_dashboard_stats(admin_id=admin_id)
            formatted_data = {
                "loc":"livequeue_cum_dashboard_cdc",
                "client_id":client_id,
                "live_queue":result_live_queue["data"],
                "dashboard": result_dashboard["data"]
            }
            await self.connection[admin_id].send_json(data=formatted_data)


    async def submitFormToAdmin(self, admin_id:str, form_id:str, data:list[dict]):
        if admin_id  in self.connection:
            result_live_queue = await db_get_live_tracking(form_id=form_id)
            result_dashboard = await db_get_dashboard_stats(admin_id=admin_id)
            formatted_data = {
                "loc": "livequeue_cum_dashboard",
                "live_queue":result_live_queue["data"],
                "dashboard": result_dashboard["data"]
            }
            await self.connection[admin_id].send_json(data=formatted_data)


    async def broadcastQueueUpdate(self, form_id:str):
        """Broadcast updated positions to all connected waiting clients for a given form.
        Efficient: one DB query, one pass to compute shared stats, then per-client sends."""
        # submissions = await db_get_all_submissions(form_id)
        # if not submissions:
        #     return

        # # --- Shared computation (one pass) ---
        # current_pos = 0
        # total_cancelled = 0
        # timing = []

        # for sub in submissions:
        #     if sub["checked"] or sub["skipped"]:
        #         current_pos += 1
        #         if sub.get("checked_time"):
        #             timing.append(sub["checked_time"])
        #     if sub["cancelled"]:
        #         total_cancelled += 1

        # # Average time per person
        # expected_time_per = 0
        # n = len(timing)
        # if n > 1:
        #     time_diff = []
        #     fmt = "%H:%M:%S"
        #     for i in range(n - 1):
        #         t1 = datetime.strptime(timing[i], fmt)
        #         t2 = datetime.strptime(timing[i + 1], fmt)
        #         diff = t2 - t1
        #         time_diff.append(diff.total_seconds() // 60)
        #     expected_time_per = sum(time_diff) // len(time_diff)

        queue_data = QUEUE.getQueueStatsAll(form_id = form_id)

        # --- Per-client position calculation and send ---
        for client_id, pos in queue_data["peoples"].items():
            # client_id = sub["client_id"]

            # # Skip clients that are explicitly skipped, cancelled, or marked as missed (Done)
            # if sub.get("missed", False) or sub["skipped"] or sub["cancelled"]:
            #     continue

            # # Only send to connected clients
            # if client_id not in self.connection:
            #     continue

            # # your_spot = (1-based index) - total_cancelled  (mirrors get_current_stats logic)
            # your_spot = (idx + 1) - total_cancelled
            # expected_time = expected_time_per * abs(your_spot - current_pos)
            if client_id in self.connection:
                formatted_data = {
                    "loc": "client_dash_position",
                    "your_spot": pos,
                    "current_pos": queue_data["current_turn"],
                    # "expected_time": expected_time
                }
                await self.connection[client_id].send_json(data=formatted_data)
    

rtc = ConnectionManager()