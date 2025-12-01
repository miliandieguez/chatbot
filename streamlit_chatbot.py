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
                    background-color: #FFFFFF !important;
                    color: #00000 !important;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
 
        elif tema == "Dark":
            [theme]
            base="light"
            primaryColor="slateBlue"
            backgroundColor="mintCream"
            secondaryBackgroundColor="darkSeaGreen"
            baseRadius="full"

            [theme.sidebar]
            backgroundColor="aliceBlue"
            secondaryBackgroundColor="skyBlue"
            baseRadius="none"


        elif tema == "Christmas":
            st.markdown("""
                <style>
                .stApp {
                    background-color: #008000;
                    color: #FF0000;
                }
                .snowflake {
                    position: fixed;
                    top: -10%;
                    color: white;
                    user-select: none;
                    pointer-events: none;
                }

                @keyframes fall {
                    0% { transform: translateY(-10vh); }
                    100% { transform: translateY(110vh); }
                }
                </style>

                <script>
                // Genera 50 flocs de neu aleatoris
                const totalFlakes = 50;

                for (let i = 0; i < totalFlakes; i++) {
                    const flake = document.createElement("div");
                    flake.className = "snowflake";
                    flake.textContent = "❄";

                    const size = Math.random() * 1.5 + 0.5;        // mida 0.5–2em
                    const left = Math.random() * 100;              // posició aleatòria
                    const duration = Math.random() * 5 + 5;        // 5–10s
                    const delay = Math.random() * 5;               // retard 0–5s

                    flake.style.left = `${left}vw`;
                    flake.style.fontSize = `${size}em`;
                    flake.style.animation = `fall ${duration}s linear infinite`;
                    flake.style.animationDelay = `${delay}s`;

                    document.body.appendChild(flake);
                }
                </script>
            """, unsafe_allow_html=True)

        elif tema == "Pink":
            st.markdown(
                """
                <style>
                .stApp {
                    background-color: #F8C8DC;
                    color: 93004F;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
        elif tema == "Ocean":
            st.markdown(
                """
                <style>
                .stApp {
                    background-color: #065588;
                    color: #A3BBE4;
                }
                </style>
                """,
                unsafe_allow_html=True
            )            


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

