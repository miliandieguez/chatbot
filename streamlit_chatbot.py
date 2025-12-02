import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

# Configuración inicial
st.set_page_config(page_title="Chatbot Básico", page_icon="🤖")
st.title("Eliseu")
st.markdown("Bienvenido a tu asitente. ¿En qué puedo ayudarte?")

conill = "https://i.ibb.co/GQ7zg6hk/conill.png"
colom ="https://i.ibb.co/xKgvdvk2/colom.png"
ratpenat = "https://i.ibb.co/tMwS20M0/ratpenat.png"
elefant = "https://i.ibb.co/275HCYYv/elefant.png"

st.image(ratpenat, width=250)


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


    if "chat_model" not in st.session_state:
        st.session_state.chat_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

        with st.expander("Modelos"):
            modelo_elegido = st.selectbox(
                "Selecciona un modelo:",
                ("gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro")
            )
            if modelo_elegido == "gemini-2.5-flash":
                st.markdown("Modelo más avanzado, ideal para tareas complejas y respuestas detalladas.")
                st.imatge(ratpenat, width = 250)
            elif modelo_elegido == "gemini-1.5-flash":
                st.markdown("Modelo equilibrado, adecuado para una amplia gama de aplicaciones.")
                st.image(conill, width = 250)
            elif modelo_elegido == "gemini-1.5-pro":
                st.markdown("Modelo optimizado para eficiencia y velocidad, ideal para respuestas rápidas.")
                st.image(elefant, width = 250)
        

    st.session_state.chat_model = ChatGoogleGenerativeAI(
        model=modelo_elegido,
        temperature=temperatura
    )


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


memory_enabled = st.sidebar.toggle("Activar memoria del chat", value=True)
if memory_enabled:
    st.sidebar.markdown("La memoria del chat está activada. El historial de tu conversación se guardará.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    with st.expander("Temas"):
        tema = st.selectbox(
            "Selecciona un tema:",
            ("Light", "Dark", "Pink", "Ocean")
            )
        set_theme(tema)

        
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []



for msg in st.session_state.mensajes:

    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)


pregunta = st.chat_input("Escribe tu mensaje:")

if pregunta:
    # Mostrar y almacenar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(pregunta)
    
    st.session_state.mensajes.append(HumanMessage(content=pregunta))

    respuesta = st.session_state.chat_model.invoke(st.session_state.mensajes)

    with st.chat_message("assistant"):
        st.markdown(respuesta.content)

    st.session_state.mensajes.append(respuesta)

