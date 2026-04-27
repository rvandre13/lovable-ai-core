from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. Carrega as variáveis de ambiente do ficheiro .env
load_dotenv()

# Verificação de segurança para garantir que a chave foi lida
minha_chave = os.getenv("GOOGLE_API_KEY")
if not minha_chave:
    print("ERRO CRÍTICO: A chave GOOGLE_API_KEY não foi encontrada no ficheiro .env!")

# 2. Inicializa a API e configura a chave do Gemini
app = FastAPI(title="Motor de IA - Lovable", version="1.0")
genai.configure(api_key=minha_chave)

# Engenharia de Contexto: Aqui definimos a instrução de sistema (personalidade)
instrucao_sistema = """Você é um assistente sênior de engenharia de software da empresa Lovable. 
Suas respostas devem ser diretas, focadas em código e estruturadas logicamente."""

# Instancia o modelo com o nosso contexto customizado
modelo = genai.GenerativeModel(
    model_name='gemini-2.5-flash', 
    system_instruction=instrucao_sistema
)

# 4. Define a estrutura da requisição
class RequisicaoChat(BaseModel):
    mensagem: str

# 5. Cria a rota de processamento com tratamento de erros
@app.post("/chat")
async def chat_com_ia(requisicao: RequisicaoChat):
    try:
        # Tenta fazer a requisição para os servidores do Google
        resposta = modelo.generate_content(requisicao.mensagem)
        return {"resposta": resposta.text}
        
    except Exception as erro_ia:
        # Se o Google devolver um erro de limite (429)
        if "429" in str(erro_ia) or "Quota" in str(erro_ia):
            mensagem_amigavel = "⚠️ Atingimos o limite de perguntas rápidas do plano gratuito. Por favor, aguarde uns 30 segundos e tente novamente!"
            return {"resposta": mensagem_amigavel}
            
        # Para outros erros desconhecidos
        return {"resposta": f"❌ Ocorreu um erro no servidor da IA: {str(erro_ia)}"}