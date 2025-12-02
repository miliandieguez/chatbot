import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

TEXTOS = {
    "Català": {
        "titulo": "Eliseu",
        "bienvenida": "Benvingut/da al teu assistent. En què et puc ajudar?",
        "personal_text": "Personalització del text",
        "tipo_letra": "Tipus de lletra",
        "medida": "Mida de lletra",
        "temperatura": "Selecciona la temperatura:",
        "tecnico": "Tècnic",
        "creativo": "Creatiu",
        "info_modelo": "Informació del model",
        "descr_modelos": """
### Selecciona el model que millor s'adapti a les teves necessitats:

- **gemini-2.5-flash**: Model avançat, ideal per a tasques complexes i respostes detallades.
- **gemini-1.5-flash**: Model equilibrat, adequat per a una àmplia gamma d'aplicacions.
- **gemini-1.5-pro**: Model optimitzat per a rapidesa i eficiència.
""",
        "select_modelo": "Selecciona un model:",
        "exportar_his": "Exportar historial com a text",
        "descargar_hist": "Descarregar historial",
        "activar_memoria": "Activar memòria del chat",
        "memoria_activada": "La memòria del chat està activada. L'historial es guardarà.",
        "temas": "Temes",
        "select_tema": "Selecciona un tema:",
        "escribe": "Escriu el teu missatge:"
    },

    "Castellano": {
        "titulo": "Eliseu",
        "bienvenida": "Bienvenido/a a tu asistente. ¿En qué puedo ayudarte?",
        "personal_text": "Personalización de texto",
        "tipo_letra": "Tipo de letra",
        "medida": "Tamaño de letra",
        "temperatura": "Selecciona temperatura:",
        "tecnico": "Técnico",
        "creativo": "Creativo",
        "info_modelo": "Información del modelo",
        "descr_modelos": """
### Selecciona el modelo que mejor se adapte a tus necesidades:

- **gemini-2.5-flash**: Modelo más avanzado, ideal para tareas complejas y respuestas detalladas.
- **gemini-1.5-flash**: Modelo equilibrado, adecuado para una amplia gama de aplicaciones.
- **gemini-1.5-pro**: Modelo optimizado para eficiencia y velocidad, ideal para respuestas rápidas.
""",
        "select_modelo": "Selecciona un modelo:",
        "exportar_his": "Exportar historial como texto",
        "descargar_hist": "Descargar historial",
        "activar_memoria": "Activar memoria del chat",
        "memoria_activada": "La memoria del chat está activada. El historial se guardará.",
        "temas": "Temas",
        "select_tema": "Selecciona un tema:",
        "escribe": "Escribe tu mensaje:"
    }
}

st.set_page_config(page_title="Eliseu Chatbot")

idioma = st.sidebar.selectbox("Idioma", ("Català", "Castellano"))
T = TEXTOS[idioma]

st.title(T["titulo"])
st.markdown(T["bienvenida"])

with st.sidebar:
    st.title("Menú")

    with st.expander(T["personal_text"]):
        font = st.selectbox(T["tipo_letra"], ["Arial", "Verdana", "Courier", "Comic Sans MS"])
        size = st.slider(T["medida"], 12, 30, 16)

    st.markdown(f"""
        <style>
        .stChatMessage div[data-testid="stMarkdownContainer"] p {{
            font-family: {font} !important;
            font-size: {size}px !important;
        }}
        </style>
    """, unsafe_allow_html=True)

    temperatura = st.slider(
        T["temperatura"],
        min_value=0.0,
        max_value=2.0,
        value=1.0,
        step=0.05
    )
    cols = st.columns(3)
    cols[0].write(T["tecnico"])
    cols[2].write(T["creativo"])

    with st.expander(T["info_modelo"]):
        st.markdown(T["descr_modelos"])

    modelo_elegido = st.selectbox(
        T["select_modelo"],
        ("gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro")
    )

    if st.sidebar.button(T["exportar_his"]):
        if "mensajes" in st.session_state and st.session_state.mensajes:
            historial_texto = "\n\n".join([msg.content for msg in st.session_state.mensajes])
            st.download_button(
                T["descargar_hist"],
                data=historial_texto,
                file_name="historial_chat.txt",
                mime="text/plain"
            )

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
        .stChatMessage div[data-testid="stMarkdownContainer"] p {{
            color: {color_texto} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

imagenes_tema = {
    "Light": "https://i.ibb.co/WNYJxvN2/colom.png",
    "Pink": "https://i.ibb.co/c0JDyMk/conill.png",
    "Ocean": "https://i.ibb.co/Q760Cbmm/peix.png",
    "Dark": "https://i.ibb.co/B5N9X0CV/ratpenat.png"
}

with st.sidebar.expander(T["temas"]):
    tema = st.selectbox(T["select_tema"], ("Light", "Dark", "Pink", "Ocean"))
    set_theme(tema)

st.image(imagenes_tema[tema], width=250)

memory_enabled = st.sidebar.toggle(T["activar_memoria"], value=True)
if memory_enabled:
    st.sidebar.markdown(T["memoria_activada"])

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

for msg in st.session_state.mensajes:
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

pregunta = st.chat_input(T["escribe"])

if pregunta:
    with st.chat_message("user"):
        st.markdown(pregunta)

    st.session_state.mensajes.append(HumanMessage(content=pregunta))

    respuesta = st.session_state.chat_model.invoke(st.session_state.mensajes)

    with st.chat_message("assistant"):
        st.markdown(respuesta.content)

    st.session_state.mensajes.append(respuesta)
