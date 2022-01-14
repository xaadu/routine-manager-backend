from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

APP_VERSION = '1'

ROOT_PATH = f'/routinemang/v{APP_VERSION}'

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


@app.get("/", tags=["Home"])
async def home():
    return {"message": "Routine Manager"}
