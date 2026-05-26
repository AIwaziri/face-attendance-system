from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import face_login

from .db import Base, engine
from .routes import users, attendance, auth_routes
from .routes import face_logout, users_list, face_attendance

from fastapi import WebSocket
from .websocket import manager


app = FastAPI(title="Face SaaS Platform")
app.include_router(face_login.router, prefix="/face")
app.include_router(face_logout.router, prefix="/face")
app.include_router(users_list.router, prefix="/users")
app.include_router(face_attendance.router, prefix="/face")
# CORS FIX (CRITICAL)
app.add_middleware(

    CORSMiddleware,

    allow_origins=[

        "http://localhost:5173",

        "http://127.0.0.1:5173"

    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)

Base.metadata.create_all(bind=engine)

app.include_router(users.router, prefix="/users")
app.include_router(attendance.router, prefix="/attendance")
app.include_router(auth_routes.router, prefix="/auth")

@app.websocket("/ws/attendance")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()
    except:
        manager.disconnect(websocket)

@app.get("/")
def home():
    return {"message": "AiWaziri FaceID SaaS API running"}