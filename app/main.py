from fastapi import FastAPI,APIRouter
from fastapi.responses import RedirectResponse
from src.db.database import get_db
from src.routers import user

app = FastAPI()

@app.get("/")
async def redirect_docs():
    return RedirectResponse("/docs")

@app.get("/hello")
async def root():
    return {"message": "Hello World"}

app.include_router(user.router)