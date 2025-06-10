import os
import httpx
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

async def generate_reflection(input_text: str, type_: str, language: str = "pt") -> str:
    try:
        # Define os prompts em português e inglês
        prompts = {
            "pt": {
                "bible": '''Por favor, analise o seguinte texto e escreva uma reflexão bíblica detalhada e inspiradora:

Texto: "{input_text}"

Sua reflexão deve:
1. Ter no maximo 2 parágrafos
2. Incluir referências bíblicas relevantes
3. Conectar o texto com ensinamentos bíblicos
4. Oferecer uma perspectiva espiritual sobre a situação
5. Terminar com uma mensagem de esperança e fé

Por favor, escreva sua reflexão agora:''',
                "psych": '''Por favor, analise o seguinte texto e escreva uma reflexão psicológica detalhada e profunda:

Texto: "{input_text}"

Sua reflexão deve:
1. Ter no maximo 2 parágrafos
2. Analisar os aspectos emocionais e psicológicos
3. Oferecer insights sobre autoconhecimento
4. Sugerir práticas para equilíbrio emocional
5. Terminar com uma mensagem motivacional

Por favor, escreva sua reflexão agora:'''
            },
            "en": {
                "bible": '''Please analyze the following text and write a detailed and inspiring biblical reflection:

Text: "{input_text}"

Your reflection should:
1. Have a maximum of 2 paragraphs
2. Include relevant biblical references
3. Connect the text with biblical teachings
4. Offer a spiritual perspective on the situation
5. End with a message of hope and faith

Please write your reflection now:''',
                "psych": '''Please analyze the following text and write a detailed and profound psychological reflection:

Text: "{input_text}"

Your reflection should:
1. Have a maximum of 2 paragraphs
2. Analyze emotional and psychological aspects
3. Offer insights about self-knowledge
4. Suggest practices for emotional balance
5. End with a motivational message

Please write your reflection now:'''
            }
        }

        # Seleciona o prompt baseado no tipo e idioma
        prompt = prompts[language][type_].format(input_text=input_text)

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        body = {
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": [
                {"role": "system", "content": "Você é um especialista em reflexões profundas e inspiradoras. Suas respostas são sempre detalhadas, bem estruturadas e significativas."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.8,
            "max_tokens": 1000,
            "top_p": 0.9,
            "frequency_penalty": 0.5,
            "presence_penalty": 0.5
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=body)
            data = response.json()
            print("Resposta da OpenRouter:", data)  # Log para depuração
            
            if "error" in data:
                error_msg = data["error"].get("message", "Erro desconhecido na API")
                print(f"Erro na API OpenRouter: {error_msg}")
                return f"Desculpe, houve um erro ao gerar a reflexão: {error_msg}"
            
            if "choices" not in data or not data["choices"]:
                print("Resposta da API sem choices:", data)
                return "Desculpe, houve um erro ao processar a resposta da API."
            
            return data["choices"][0]["message"]["content"].strip()
            
    except Exception as e:
        print(f"Erro ao gerar reflexão: {str(e)}")
        return f"Desculpe, ocorreu um erro ao gerar sua reflexão. Por favor, tente novamente mais tarde."
