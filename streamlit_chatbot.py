import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

# Configuración inicial
st.set_page_config(page_title="Chatbot Básico", page_icon="🤖")
st.title("Eliseu")
st.markdown("Bienvenido a tu asistente. ¿En qué puedo ayudarte?")

# Crear espacio de session_state
if "chat_model" not in st.session_state:
    st.session_state.chat_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Sidebar
with st.sidebar:
    st.title("Menú")

    temperatura = st.slider(
        "Selecciona temperatura:",
        min_value=0.0,
        max_value=2.0,
        value=1.0,
        step=0.05
    )

    with st.expander("Modelos"):
        modelo_elegido = st.selectbox(
            "Selecciona un modelo:",
            ("gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro")
        )

    # Quan l’usuari canvia el model o la temperatura, regenerem el model
    st.session_state.chat_model = ChatGoogleGenerativeAI(
        model=modelo_elegido,
        temperature=temperatura
    )

# Historial de mensajes
for msg in st.session_state.mensajes:
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

# Entrada del usuario
pregunta = st.chat_input("Escribe tu mensaje:")

if pregunta:
    with st.chat_message("user"):
        st.markdown(pregunta)

    st.session_state.mensajes.append(HumanMessage(content=pregunta))

    respuesta = st.session_state.chat_model.invoke(st.session_state.mensajes)

    with st.chat_message("assistant"):
        st.markdown(respuesta.content)

    st.session_state.mensajes.append(respuesta)
