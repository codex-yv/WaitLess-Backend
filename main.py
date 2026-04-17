from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from app.routes.auth import router as authentication
from app.routes.home import router as homepage

from app.routes.admin.customForm import router as admin_forms
from app.routes.admin.dashboard import router as admin_dashboard
from app.routes.admin.tracking import router as admin_tracking
from app.routes.admin.forms import router as admin_form
from app.routes.clients.dashboard import router as client_dashboard
from app.routes.clients.forms import router as client_form

from communication.RTC import rtc
from config.environment import ALLOWED_ORIGINS

app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authentication)
app.include_router(homepage)

app.include_router(admin_forms)
app.include_router(admin_dashboard)
app.include_router(admin_tracking)
app.include_router(admin_form)

app.include_router(client_form)
app.include_router(client_dashboard)

@app.api_route("/", methods=["HEAD"], operation_id="welcome_get")
async def welcome_head():
    return {"Message": "Ok"}

@app.get("/")
def checkHealth():
    return {
        "message": "Queue-Eliminator Backend is Live."
    }

@app.websocket("/ws/{req_id}")
async def realTimeConnections(req_id:str, websocket:WebSocket):
    await rtc.connect(req_id=req_id, websocket=websocket)
    print(f"User:{req_id} is connected to the server at instance:{websocket}")
    try:
        while True:
            data = await websocket.receive_json()

    except WebSocketDisconnect:
        await rtc.disconnect(req_id)
        print(f"User:{req_id} is leaved the server at instance:{websocket}")
