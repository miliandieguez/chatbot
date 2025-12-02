import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

# Configuración inicial
st.set_page_config(page_title="Chatbot Básico", page_icon="🤖")
st.title("Eliseu")
st.markdown("Bienvenido a tu asistente. ¿En qué puedo ayudarte?")

# Imatges
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

    # Explicació del model
    st.markdown("""
### Selecciona el modelo que mejor se adapte a tus necesidades:

- **gemini-2.5-flash**: Modelo más avanzado, ideal para tareas complejas y respuestas detalladas.
- **gemini-1.5-flash**: Modelo equilibrado, adecuado para una amplia gama de aplicaciones.
- **gemini-1.5-pro**: Modelo optimizado para eficiencia y velocidad, ideal para respuestas rápidas.
""")

    modelo_elegido = st.selectbox(
        "Selecciona un modelo:",
        ("gemini-2.5-flash","gemini-1.5-flash", "gemini-1.5-pro")
    )

# Crear el chat_model con la selección actual
st.session_state.chat_model = ChatGoogleGenerativeAI(
    model=modelo_elegido,
    temperature=temperatura
)

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

# Inicialitzar històric
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Mostrar històric
for msg in st.session_state.mensajes:
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

# Entrada de l’usuari
pregunta = st.chat_input("Escribe tu mensaje:")

if pregunta:
    with st.chat_message("user"):
        st.markdown(pregunta)

    st.session_state.mensajes.append(HumanMessage(content=pregunta))

    respuesta = st.session_state.chat_model.invoke(st.session_state.mensajes)

    with st.chat_message("assistant"):
        st.markdown(respuesta.content)

    st.session_state.mensajes.append(respuesta)
