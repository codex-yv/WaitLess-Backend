from unittest import skip
from app.database.forms import db_get_all_submissions #db_get_current_stats
from datetime import datetime


class Queue:
    def __init__(self):
        # temporary storage for form-wise submission
        # format : {form_id:{"current_turn": xxx, "peoples":{client_id: yyy}}}
        self.queue_data = {} 

        # temporary storage for skipped submissions
        # format: [client_id]
        self.skipped = []

    async def populateQueue(self, form_id:str):
    
        # populates the form-wise submissions for a given form_id

        submissions = await db_get_all_submissions(form_id)

        # calculating current_turn
        turn = 0
        for submission in submissions:
            if submission["checked"] or submission["skipped"]:
                turn +=1


        self.queue_data[form_id] = {"current_turn": turn, "peoples":{}}
        
        # calculating current_pos
        pos = 1
        for submission in submissions:
            if not submission["cancelled"]:
                self.queue_data[form_id]["peoples"][submission["client_id"]] = pos
                pos+=1
        

    async def addNewPerson(self, form_id: str, client_id: str):
        # adds new person/submission in queue_data

        if form_id in self.queue_data:
            # calculating position of newly added person
            pos = 1
            for people in self.queue_data[form_id]["peoples"]:
                pos+=1

            self.queue_data[form_id]["peoples"][client_id] = pos
        else:
            # populating the queue_data if form_id doesn't exist.
            await self.populateQueue(form_id)

    async def cancelRegistration(self,form_id:str, client_id:str):
        # cancelled submission is removed from queue_data

        if form_id in self.queue_data:
            # calculating position of submission after cancellation
            decrement = False
            for people in self.queue_data[form_id]["peoples"]:
                if decrement:
                    self.queue_data[form_id]["peoples"][people] -= 1

                if people == client_id:
                    decrement = True
                    
            # removing client from submission
            del self.queue_data[form_id]["peoples"][client_id]
        else:
            await self.populateQueue(form_id)

    async def callNext(self, form_id):
        if form_id in self.queue_data:
            self.queue_data[form_id]["current_turn"] +=1
        else:
            await self.populateQueue(form_id)

    async def skipNext(self, client_id:str, form_id:str):
        if form_id in self.queue_data:
            self.queue_data[form_id]["current_turn"] +=1
            self.skipped.append(client_id)
        else:
            await self.populateQueue(form_id)

    async def undoSkip(self, form_id, client_id:str):
        if form_id in self.queue_data:
            self.queue_data[form_id]["current_turn"] -=1
            self.skipped.remove(client_id)
        else:
            await self.populateQueue(form_id)

    async def getQueueStats(self, form_id:str, client_id:str) -> dict:
        if form_id in self.queue_data:
            try:
                info = {
                    "current_turn":self.queue_data[form_id]["current_turn"],
                    "current_pos": self.queue_data[form_id]["peoples"][client_id], # it will generate key error when if booking is cancelled.
                    "skipped":client_id in self.skipped
                } 
            except KeyError as e:
                # it means cancelled
                print(e)
                info = {
                    "current_turn": None,
                    "current_pos": None,
                    "skipped": False
                }
            finally:
                return info
            
        else:
            await self.populateQueue(form_id)
            return await self.getQueueStats(form_id, client_id)
        
    def getQueueStatsAll(self, form_id: str):
        return self.queue_data[form_id]
    
QUEUE = Queue()

# <--------------- Replace the use of below function from above classe ---------------->

async def get_current_stats(client_id:str, form_id:str):
    result = await db_get_all_submissions(form_id)
    if result:
        skipped = False
        cancelled = False
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
                skipped = client["skipped"]
                cancelled = client["cancelled"]

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

            expected_time = avg_time * abs(your_spot-current_pos)
        
        return your_spot, current_pos, expected_time, notification, template, skipped, cancelled

    else:
        return 0, 0, 0, [], [], False, False
