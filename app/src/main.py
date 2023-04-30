from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/")
async def redirect_docs():
    return RedirectResponse("/docs")

@app.get("/hello")
async def root():
    return {"message": "Hello World"}