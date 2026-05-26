from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import face_login

from .db import Base, engine
from .routes import users, attendance, auth_routes
from .websocket import router as ws_router
from .routes import face_logout, users_list




app = FastAPI(title="Face SaaS Platform")
app.include_router(face_login.router, prefix="/face")
app.include_router(face_logout.router, prefix="/face")
app.include_router(users_list.router, prefix="/users")
# CORS FIX (CRITICAL)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(users.router, prefix="/users")
app.include_router(attendance.router, prefix="/attendance")
app.include_router(auth_routes.router, prefix="/auth")
app.include_router(ws_router)


@app.get("/")
def home():
    return {"message": "Face SaaS API running"}