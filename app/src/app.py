from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .db.userdbmanager import UserDatabaseManager

from .routes import (
    auth,
    course,
    lecturer,
)


app = FastAPI()

APP_VERSION = '1'

ROOT_PATH = f'/routineman/v{APP_VERSION}'

app = FastAPI(
    title="Routine Manager API",
    description="This is a small API Project For Managing Routine",
    version=APP_VERSION,
)
app.mount(ROOT_PATH, app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = UserDatabaseManager()

@app.get("/", response_description="Title with Payload", tags=["Home"])
async def home():
    user_count = await db.num_of_user
    return JSONResponse({"message": "Routine Manager", "payload": {"user_count": user_count}})


app.include_router(auth.router)
app.include_router(course.router)
app.include_router(lecturer.router)
