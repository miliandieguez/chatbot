import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

# Configuración inicial
st.set_page_config(page_title="Chatbot Básico", page_icon="🤖")
st.title("Chatbot")
st.markdown("Bienvenido a este *chatbot* construido con LangChain + Streamlit.")

chat_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Menú lateral

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
            ("Light", "Dark", "Christmas", "Pink", "Ocean")
        )
        if tema == "Light":
            st.markdown(
                """
                <style>
                .stApp {
                    background-color: #FFFFFF;
                    color: #000000;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
        elif tema == "Dark":
            st.markdown(
                """
                <style>
                .stApp {
                    background-color: #000000;
                    color: #FFFFFF;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
        elif tema == "Christmas":
            st.markdown("""
                <style>
                .snowflake {
                color: black;
                font-size: 1.5em;
                position: fixed;
                top: -10%;
                animation: fall 10s linear infinite;
                }

                @keyframes fall {
                0% {top: -10%;}
                00% {top: 110%;}
                }
                </style>

                <div class="snowflake">❄</div>
                <div class="snowflake" style="left:20%">❄</div>
                <div class="snowflake" style="left:40%">❄</div>
                <div class="snowflake" style="left:60%">❄</div>
                <div class="snowflake" style="left:80%">❄</div>
                """, unsafe_allow_html=True)




# Inicializar el historial de mensajes en session_state
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []


# Renderizar historial existente
for msg in st.session_state.mensajes:

    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

# Input de usuario
pregunta = st.chat_input("Escribe tu mensaje:")

if pregunta:
    # Mostrar y almacenar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(pregunta)
    
    st.session_state.mensajes.append(HumanMessage(content=pregunta))

    respuesta = chat_model.invoke(st.session_state.mensajes)

    with st.chat_message("assistant"):
        st.markdown(respuesta.content)

    st.session_state.mensajes.append(respuesta)

