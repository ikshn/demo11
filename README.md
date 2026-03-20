# demo11 - Emotion Detect (Text + Speech)

This repo contains a vibrant, picture-rich FastAPI + Jinja web UI for **emotion detection** from:

- **Text** (type/paste a message)
- **Speech** (upload an audio file)

The current emotion predictors are lightweight **stubs** so the app runs without heavy model dependencies. You can swap them later with real NLP / audio models.

## Project structure

```text
.
├── app/
│   ├── api/
│   │   ├── speech_routes.py
│   │   └── text_routes.py
│   ├── core/
│   │   └── web.py
│   └── services/
│       ├── emotion_labels.py
│       ├── speech_emotion.py
│       └── text_emotion.py
│   └── main.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── speech.html
│   ├── text.html
│   └── results.html
├── static/
│   ├── css/styles.css
│   └── js/app.js
├── tests/
└── requirements.txt
```

## Run it

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open: `http://localhost:8000`
