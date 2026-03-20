from fastapi import APIRouter, Form, Request

from app.core.web import templates
from app.services.text_emotion import predict_text_emotion

router = APIRouter()


@router.get("/text")
def text_form(request: Request):
    return templates.TemplateResponse("text.html", {"request": request})


@router.post("/text/predict")
def text_predict(request: Request, text: str = Form(...)):
    result = predict_text_emotion(text)
    return templates.TemplateResponse(
        "results.html",
        {
            "request": request,
            "modality": "text",
            "input_text": text,
            "input_caption": "Text you entered",
            "result": result,
        },
    )


@router.post("/api/text/predict")
def text_predict_api(text: str = Form(...)):
    # API variant for JS/future integrations.
    return predict_text_emotion(text)

