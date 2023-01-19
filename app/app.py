from fastapi import FastAPI
from .models import users
from .database.database import engine
from .routers import users_router

users.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(users_router.router)
