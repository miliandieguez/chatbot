import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage


st.set_page_config(page_title="Chatbot Básico", page_icon="🤖")
st.title("Eliseu")
st.markdown("Bienvenido a tu asistente. ¿En qué puedo ayudarte?")


def set_theme(tema):
    if tema == "Light":
        color_fons = "#FFFFFF"
        color_text = "#000000"
    elif tema == "Dark":
        color_fons = "#1E1E1E"
        color_text = "#FFFFFF"
    elif tema == "Pink":
        color_fons = "#FFC0CB"
        color_text = "#000000"
    elif tema == "Ocean":
        color_fons = "#87CEFA"
        color_text = "#000000"

    st.markdown(
        f"""
        <style>
        .stApp, .main, .block-container {{
            background-color: {color_fons} !important;
            color: {color_text} !important;
        }}
        header, footer {{
            background-color: {color_fons} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


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


    with st.expander("Temas"):
        tema = st.selectbox(
            "Selecciona un tema:",
            ("Light", "Dark", "Pink", "Ocean")
        )
        set_theme(tema)


    with st.expander("Modelos"):
        modelo_elegido = st.selectbox(
            "Selecciona un modelo:",
            ("gemini-2.5-flash", "gemini-1", "otro-modelo")
        )


if "chat_model" not in st.session_state or st.session_state.chat_model.model != modelo_elegido:
    st.session_state.chat_model = ChatGoogleGenerativeAI(model=modelo_elegido)

chat_model = st.session_state.chat_model


if "mensajes" not in st.session_state:
    st.session_state.mensajes = []


for msg in st.session_state.mensajes:
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)


pregunta = st.chat_input("Escribe tu mensaje:")

if pregunta:
    
    with st.chat_message("user"):
        st.markdown(pregunta)

    st.session_state.mensajes.append(HumanMessage(content=pregunta))

   
    respuesta = chat_model.invoke(
        st.session_state.mensajes,
        temperature=temperatura
    )

    with st.chat_message("assistant"):
        st.markdown(respuesta.content)

    st.session_state.mensajes.append(respuesta)
