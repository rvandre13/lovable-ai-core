import streamlit as st
import requests

# Configuração da página
st.set_page_config(page_title="Lovable IA", page_icon="🤖")
st.title("Lovable IA - Assistente de Engenharia")

# Inicializa o histórico de chat na memória da interface
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

# Exibe as mensagens antigas na tela
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Caixa de texto para o usuário digitar
pergunta = st.chat_input("Digite sua dúvida de programação...")

if pergunta:
    # Mostra a pergunta do usuário na tela
    with st.chat_message("user"):
        st.markdown(pergunta)
    # Salva no histórico
    st.session_state.mensagens.append({"role": "user", "content": pergunta})

    # Mostra o status do assistente e chama a nossa API
    with st.chat_message("assistant"):
        resposta_interface = st.empty()
        resposta_interface.markdown("Pensando...")
        
        try:
            # Envia a requisição POST para o nosso back-end FastAPI
            res = requests.post("https://lovable-ai-core.onrender.com/chat", json={"mensagem": pergunta})
            
            if res.status_code == 200:
                texto_resposta = res.json()["resposta"]
                # Exibe a resposta final e salva no histórico
                resposta_interface.markdown(texto_resposta)
                st.session_state.mensagens.append({"role": "assistant", "content": texto_resposta})
            else:
                resposta_interface.markdown("Erro na comunicação com a API do back-end.")
        except Exception as e:
            resposta_interface.markdown(f"Erro: Verifique se o FastAPI está rodando. Detalhe: {e}")