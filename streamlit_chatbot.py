import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_llama import ChatLlama  # Exemple, depèn de la llibreria que tinguis
from langchain_core.messages import AIMessage, HumanMessage

# Configuración inicial
st.set_page_config(page_title="Chatbot Básico", page_icon="🤖")
st.title("Eliseu")
st.markdown("Bienvenido a tu asistente. ¿En qué puedo ayudarte?")

conill = "https://i.ibb.co/GQ7zg6hk/conill.png"
colom = "https://i.ibb.co/xKgvdvk2/colom.png"
ratpenat = "https://i.ibb.co/tMwS20M0/ratpenat.png"
elefant = "https://i.ibb.co/275HCYYv/elefant.png"

st.image(ratpenat, width=250)

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
    cols = st.columns(3)
    cols[0].write("Técnico")
    cols[2].write("Creativo")

    # Explicació del model
    st.markdown("""
### Selecciona el modelo que mejor se adapte a tus necesidades:

- **gemini-2.5-flash**: Modelo más avanzado, ideal para tareas complejas y respuestas detalladas.
- **openai-gpt-3.5**: Modelo equilibrado de OpenAI, requiere API Key en la variable de entorno OPENAI_API_KEY.
- **openai-gpt-4**: Modelo más avanzado de OpenAI, requiere API Key.
- **llama**: Modelo LLaMA local o API, requiere configuración propia.
""")
    modelo_elegido = st.selectbox(
        "Selecciona un modelo:",
        ("gemini-2.5-flash", "openai-gpt-3.5", "openai-gpt-4", "llama")
    )

# Crear el chat_model según modelo seleccionado
try:
    if modelo_elegido == "gemini-2.5-flash":
        st.session_state.chat_model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=temperatura
        )
    elif modelo_elegido.startswith("openai"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.error("Error: No tienes la API Key de OpenAI configurada en la variable OPENAI_API_KEY.")
        else:
            st.session_state.chat_model = ChatOpenAI(
                model_name=modelo_elegido.replace("openai-", ""),
                temperature=temperatura,
                openai_api_key=api_key
            )
    elif modelo_elegido == "llama":
        api_key = os.getenv("LLAMA_API_KEY")  # Depèn de com tinguis configurat LLaMA
        if not api_key:
            st.error("Error: No tienes la API Key de LLaMA configurada en la variable LLAMA_API_KEY.")
        else:
            st.session_state.chat_model = ChatLlama(
                model="llama",
                temperature=temperatura,
                api_key=api_key
            )
except Exception as e:
    st.error(f"Error al inicializar el modelo: {e}")

# Temas
def set_theme(tema):
    if tema == "Light":
        color_fondo = "#FFFFFF"
        color_texto = "#000000"
    elif tema == "Dark":
        color_fondo = "#1E1E1E"
        color_texto = "#FFFFFF"
    elif tema == "Pink":
        color_fondo = "#FFE2E7"
        color_texto = "#87374F"
    elif tema == "Ocean":
        color_fondo = "#2E556D"
        color_texto = "#BAE0ED"

    st.markdown(
        f"""
        <style>
        .stApp, .main, .block-container {{
            background-color: {color_fondo} !important;
            color: {color_texto} !important;
        }}
        header, footer {{
            background-color: {color_fondo} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

with st.sidebar:
    with st.expander("Temas"):
        tema = st.selectbox(
            "Selecciona un tema:",
            ("Light", "Dark", "Pink", "Ocean")
        )
        set_theme(tema)

# Memòria
memory_enabled = st.sidebar.toggle("Activar memoria del chat", value=True)
if memory_enabled:
    st.sidebar.markdown("La memoria del chat está activada. El historial de tu conversación se guardará.")

# Inicializar historial
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Mostrar historial
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

    # Generar respuesta solo si chat_model existe
    if "chat_model" in st.session_state:
        respuesta = st.session_state.chat_model.invoke(st.session_state.mensajes)
        with st.chat_message("assistant"):
            st.markdown(respuesta.content)
        st.session_state.mensajes.append(respuesta)
