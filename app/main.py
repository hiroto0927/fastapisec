from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.routers import user, auth

app = FastAPI()


@app.get("/")
async def redirect_docs():
    return RedirectResponse("/docs")


app.include_router(user.router)
app.include_router(auth.router)
