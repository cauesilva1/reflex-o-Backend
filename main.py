from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai.coach import generate_reflection
from ai.affirmations import generate_affirmation

app = FastAPI()

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens em desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos
    allow_headers=["*"],  # Permite todos os headers
)

class ReflectionRequest(BaseModel):
    input_text: str
    type: str  # "bible" ou "psych"
    language: str = "pt"  # "pt" ou "en", padrão é "pt"

class AffirmationRequest(BaseModel):
    mood: str

@app.get("/")
async def root():
    return {"message": "API Reflexão Diária funcionando!"}

@app.post("/generate-reflection")
async def generate_reflection_endpoint(req: ReflectionRequest):
    reflection = await generate_reflection(req.input_text, req.type, req.language)
    return {"reflection": reflection}

@app.post("/generate-affirmation")
async def generate_affirmation_endpoint(req: AffirmationRequest):
    affirmation = await generate_affirmation(req.mood)
    return {"affirmation": affirmation}
