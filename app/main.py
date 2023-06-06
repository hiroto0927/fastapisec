from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.routers import *
from src.routers.health_check import router


app = FastAPI()


@app.get("/")
async def redirect_docs():
    return RedirectResponse("/docs")


app.include_router(router)
app.include_router(user_router)
app.include_router(auth_router)
