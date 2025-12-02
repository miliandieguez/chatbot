import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

# Configuración inicial
st.set_page_config(page_title="Chatbot Básico", page_icon="🤖")
st.title("Eliseu")
st.markdown("Bienvenido a tu asistente. ¿En qué puedo ayudarte?")

# Sidebar: seleccionar font i mida
with st.sidebar.expander("Personalización de texto"):
    st.title("Menú")
    font = st.selectbox("Tipo de letra", ["Arial", "Verdana", "Courier", "Comic Sans MS"])
    size = st.slider("Tamaño de letra", 12, 30, 16)

st.markdown(f"""
    <style>
    .stChatMessage div[data-testid="stMarkdownContainer"] p {{
        font-family: {font} !important;
        font-size: {size}px !important;
    }}
    </style>
""", unsafe_allow_html=True)

with st.sidebar:

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

    with st.expander("Información del modelo"):
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
    if st.sidebar.button("Exportar historial como texto"):
        if st.session_state.mensajes:
        # Crear un text pla amb tots els missatges
            historial_texto = "\n\n".join([msg.content for msg in st.session_state.mensajes])
        
        st.download_button(
            "Descargar historial",
            data=historial_texto,
            file_name="historial_chat.txt",
            mime="text/plain"
        )
    with st.expander("Personalizar avatares"):
        color_usuario = st.color_picker("Color del avatar del usuario", "#1E90FF")
        color_bot = st.color_picker("Color del avatar del chatbot", "#FF4500")

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
        /* Cambiar color del texto dentro de los chat messages */
        .stChatMessage div[data-testid="stMarkdownContainer"] p {{
            color: {color_texto} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Definir les imatges per tema
imagenes_tema = {
    "Light": "https://i.ibb.co/WNYJxvN2/colom.png",
    "Pink": "https://i.ibb.co/c0JDyMk/conill.png",
    "Ocean": "https://i.ibb.co/Q760Cbmm/peix.png",
    "Dark": "https://i.ibb.co/B5N9X0CV/ratpenat.png"
}

avatars_tema = {
    "Light": {
        "usuario": "https://i.ibb.co/WNYJxvN2/colom.png",
        "bot": "https://i.ibb.co/tMwS20M0/ratpenat.png"
    },
    "Dark": {
        "usuario": "https://i.ibb.co/c0JDyMk/conill.png",
        "bot": "https://i.ibb.co/275HCYYv/elefant.png"
    },
    "Pink": {
        "usuario": "https://i.ibb.co/Q760Cbmm/peix.png",
        "bot": "https://i.ibb.co/B5N9X0CV/ratpenat.png"
    },
    "Ocean": {
        "usuario": "https://i.ibb.co/XfYvJrz5/ratpenat.png",
        "bot": "https://i.ibb.co/GQ7zg6hk/conill.png"
    }
}


# Selector de tema al sidebar
with st.sidebar.expander("Temas"):
    tema = st.selectbox(
        "Selecciona un tema:",
        ("Light", "Dark", "Pink", "Ocean")
    )
    set_theme(tema)

# Mostrar la imatge corresponent al tema
st.image(imagenes_tema[tema], width=250)


# Memòria
memory_enabled = st.sidebar.toggle("Activar memoria del chat", value=True)
if memory_enabled:
    st.sidebar.markdown("La memoria del chat está activada. El historial de tu conversación se guardará.")

# Inicialitzar històric
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

for msg in st.session_state.mensajes:
    if isinstance(msg, HumanMessage):
        st.markdown(f'<img src="{avatars_tema[tema]["usuario"]}" width="40" style="vertical-align: middle; margin-right:5px;"> {msg.content}', unsafe_allow_html=True)
    else:
        st.markdown(f'<img src="{avatars_tema[tema]["bot"]}" width="40" style="vertical-align: middle; margin-right:5px;"> {msg.content}', unsafe_allow_html=True)

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
