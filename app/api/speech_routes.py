from fastapi import APIRouter, File, Request, UploadFile, Form

from app.core.web import templates
from app.services.speech_emotion import predict_speech_emotion

router = APIRouter()


@router.get("/speech")
def speech_form(request: Request):
    return templates.TemplateResponse("speech.html", {"request": request})


@router.post("/speech/predict")
async def speech_predict(request: Request, audio: UploadFile = File(...), language: str = Form("en")):
    # NOTE: `language` is accepted for future model upgrades; this stub ignores it.
    audio_bytes = await audio.read()
    result = predict_speech_emotion(audio_bytes)
    return templates.TemplateResponse(
        "results.html",
        {
            "request": request,
            "modality": "speech",
            "input_text": None,
            "input_caption": f"Speech ({language})",
            "result": result,
        },
    )


@router.post("/api/speech/predict")
async def speech_predict_api(audio: UploadFile = File(...), language: str = Form("en")):
    _ = language
    audio_bytes = await audio.read()
    return predict_speech_emotion(audio_bytes)

