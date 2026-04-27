import google.generativeai as genai
import os
from dotenv import load_dotenv

# Carrega a chave
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

print("Buscando modelos disponíveis para a sua chave...\n")

# Lista todos os modelos e filtra apenas os que geram texto
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)