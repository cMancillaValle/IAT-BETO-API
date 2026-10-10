from pathlib import Path

import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from transformers import AutoModelForSequenceClassification, AutoTokenizer


# Configuración
BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "beto-odio-limpio"
MAX_LENGTH = 128

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Cargar el modelo una sola vez
if not MODEL_DIR.is_dir():
    raise RuntimeError(f"No se encontró el modelo en: {MODEL_DIR}")

tokenizer = AutoTokenizer.from_pretrained(str(MODEL_DIR))
model = AutoModelForSequenceClassification.from_pretrained(str(MODEL_DIR))
model.to(DEVICE)
model.eval()

app = FastAPI(
    title="BETO - Clasificador de comentarios",
    description=(
        "API experimental de clasificación de texto en español. "
        "Las clases corresponden a las etiquetas aprendidas durante el entrenamiento."
    ),
    version="1.0.0",
)


class PredictionRequest(BaseModel):
    texto: str = Field(
        min_length=1,
        max_length=5000,
        description="Comentario en español que se desea clasificar.",
    )


@app.get("/")
def root():
    return {
        "mensaje": "API de BETO funcionando",
        "documentacion": "/docs",
        "dispositivo": str(DEVICE),
    }


@app.get("/health")
def health():
    return {
        "estado": "ok",
        "modelo_cargado": True,
        "dispositivo": str(DEVICE),
    }


@app.post("/predict")
def predict(request: PredictionRequest):
    texto = request.texto.strip()

    if not texto:
        raise HTTPException(
            status_code=422,
            detail="El comentario no puede estar vacío.",
        )

    inputs = tokenizer(
        texto,
        return_tensors="pt",
        truncation=True,
        max_length=MAX_LENGTH,
    )
    inputs = {name: tensor.to(DEVICE) for name, tensor in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        probabilities = torch.softmax(outputs.logits, dim=1)[0].cpu().tolist()

    predicted_class = int(torch.argmax(outputs.logits, dim=1).item())

    return {
        "clase_predicha": f"CLASE_{predicted_class}",
        "probabilidades": {
            "CLASE_0": round(probabilities[0], 6),
            "CLASE_1": round(probabilities[1], 6),
        },
        "dispositivo": str(DEVICE),
        "advertencia": (
            "Resultado experimental basado en las etiquetas del conjunto de "
            "entrenamiento; no constituye una determinación definitiva de "
            "discurso de odio."
        ),
    }