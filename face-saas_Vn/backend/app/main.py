from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import Base, engine
from .routes import face_logout, users_list, face_attendance, employees, users, attendance, auth_routes, face_login_routes, analytics

from fastapi import WebSocket
from .websocket import manager

app = FastAPI(title="AiWaziri FaceID SaaS Platform")
app.include_router(face_login_routes.router, prefix="/face")
app.include_router(face_logout.router, prefix="/face")
app.include_router(users_list.router, prefix="/users")
app.include_router(face_attendance.router, prefix="/face")
app.include_router(users.router, prefix="/users")
app.include_router(attendance.router, prefix="/attendance")
app.include_router(auth_routes.router, prefix="/auth")
app.include_router(employees.router, prefix="/employees")
app.include_router(analytics.router, prefix="/analytics")



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