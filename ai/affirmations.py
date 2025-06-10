import os
import httpx
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

async def generate_affirmation(mood: str) -> str:
    prompt = f"Crie uma afirmação positiva e personalizada para alguém que está se sentindo {mood}. Seja motivacional e encorajador."

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {"role": "system", "content": "Você é um gerador de afirmações positivas e motivacionais."},
            {"role": "user", "content": prompt}
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=body)
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
