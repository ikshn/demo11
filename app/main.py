from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app.api.speech_routes import router as speech_router
from app.api.text_routes import router as text_router
from app.core.web import templates


app = FastAPI(title="Emotion Detect (Text + Speech)", version="0.1.0")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(text_router)
app.include_router(speech_router)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

