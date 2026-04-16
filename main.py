from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.routes.auth import router as authentication
from app.routes.home import router as homepage

from app.routes.admin.customForm import router as admin_forms
from app.routes.admin.dashboard import router as admin_dashboard
from app.routes.admin.tracking import router as admin_tracking
from app.routes.admin.forms import router as admin_form
from app.routes.clients.dashboard import router as client_dashboard
from app.routes.clients.forms import router as client_form

app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
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