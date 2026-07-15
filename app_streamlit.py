"""
app_streamlit.py — Interfaz web Streamlit para el Chatbot Asesor Veltri Tecnologic.

Uso:
    streamlit run app_streamlit.py

Importa directamente la lógica del orquestador existente (procesar_mensaje).
El modo terminal (python orchestrator.py) sigue funcionando sin cambios.
"""

import time
import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# Configuración de página (debe ser lo primero antes de cualquier st.*)
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Veltri Tecnologic — Asesor Inteligente",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# Estilos CSS personalizados (tema oscuro gamer/tech)
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
/* ── Importar fuente premium ─────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

/* ── Variables de color ──────────────────────────────────────── */
:root {
    --purple-main:  #7c3aed;
    --purple-light: #a855f7;
    --blue-accent:  #3b82f6;
    --cyan-glow:    #06b6d4;
    --bg-dark:      #0f0e17;
    --bg-card:      #1a1830;
    --bg-input:     #1e1c30;
    --text-primary: #f0edff;
    --text-muted:   #9ca3af;
    --border:       rgba(124, 58, 237, 0.25);
    --glow:         rgba(124, 58, 237, 0.15);
}

/* ── Fondo global ────────────────────────────────────────────── */
.stApp {
    background: linear-gradient(135deg, #0f0e17 0%, #13112a 50%, #0f0e17 100%);
    font-family: 'Inter', sans-serif;
    color: var(--text-primary);
}

/* ── Sidebar ─────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #13112a 0%, #0f0e17 100%);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

/* ── Mensajes del chat ───────────────────────────────────────── */
[data-testid="stChatMessage"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 4px 12px;
    margin-bottom: 10px;
    backdrop-filter: blur(8px);
    transition: box-shadow 0.2s ease;
}
[data-testid="stChatMessage"]:hover {
    box-shadow: 0 0 20px var(--glow);
}
[data-testid="stChatMessage"] * {
    color: var(--text-primary) !important;
}

/* ── Burbuja del usuario ─────────────────────────────────────── */
[data-testid="stChatMessage"][data-testid*="user"] {
    border-color: rgba(59, 130, 246, 0.3);
}

/* ── Input de chat ───────────────────────────────────────────── */
[data-testid="stChatInput"] {
    border: 1px solid #4b5563 !important;
    border-radius: 12px !important;
}
[data-testid="stChatInput"] textarea {
    background: var(--bg-input) !important;
    border: none !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    width: 100% !important;
}
[data-testid="stChatInput"] textarea:focus {
    border: none !important;
    outline: none !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #9ca3af !important;
    box-shadow: 0 0 12px rgba(156, 163, 175, 0.3) !important;
}


/* ── Botones ─────────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, var(--purple-main), var(--blue-accent)) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    transition: opacity 0.2s ease, transform 0.1s ease !important;
}
.stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Métricas ────────────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: rgba(124, 58, 237, 0.08);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 8px 12px;
}
[data-testid="stMetricLabel"] {
    color: var(--text-muted) !important;
    font-size: 0.75rem !important;
}
[data-testid="stMetricValue"] {
    color: var(--purple-light) !important;
    font-weight: 700 !important;
}

/* ── Separadores ─────────────────────────────────────────────── */
hr {
    border-color: var(--border) !important;
}

/* ── Scrollbar ───────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: var(--purple-main);
    border-radius: 3px;
}

/* ── Badge de handoff ────────────────────────────────────────── */
.handoff-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: linear-gradient(135deg, rgba(124,58,237,0.2), rgba(59,130,246,0.2));
    border: 1px solid rgba(124,58,237,0.4);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.78rem;
    color: #c4b5fd;
    margin: 6px 0 10px;
    font-weight: 500;
}

/* ── Título en header ────────────────────────────────────────── */
.veltri-header {
    text-align: center;
    padding: 10px 0 4px;
}
.veltri-header h1 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.9rem !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, #a855f7, #3b82f6, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 2px !important;
}
.veltri-header p {
    color: var(--text-muted);
    font-size: 0.9rem;
    margin: 0;
}

/* ── Agente activo pill ──────────────────────────────────────── */
.agent-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(124,58,237,0.15);
    border: 1px solid rgba(124,58,237,0.35);
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 0.82rem;
    font-weight: 600;
    color: #c4b5fd;
    margin: 4px 0;
}
/* ── Inputs de texto (fix color rojo) ────────────────────── */
input[type="text"],
input[type="password"],
textarea {
    border: 1px solid #4b5563 !important;
    background: var(--bg-input) !important;
    color: var(--text-primary) !important;
}
input[type="text"]:focus,
input[type="password"]:focus,
textarea:focus {
    border-color: #9ca3af !important;
    box-shadow: 0 0 8px rgba(156, 163, 175, 0.2) !important;
}

/* ── Todos los widgets con borde ────────────────────────── */
[data-testid="stTextInput"] {
    border: 1px solid #4b5563 !important;
}
[data-testid="stTextInput"]:focus-within {
    border-color: #9ca3af !important;
}

/* ── Select boxes y otros inputs ────────────────────────── */
.stSelectbox,
.stMultiSelect,
.stDateInput,
.stTimeInput {
    border: 1px solid #4b5563 !important;
}

/* ── Remover rojo de error/enfoque de form elements ────── */
input:invalid,
textarea:invalid,
select:invalid {
    border-color: #4b5563 !important;
}
input:valid,
textarea:valid,
select:valid {
    border-color: #4b5563 !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Inicializar el orquestador (solo una vez por sesión)
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_resource(show_spinner="⚙️ Iniciando sistema multiagente...", hash_funcs={str: lambda x: x})
def _cargar_orquestador(api_key: str):
    """Importa el orquestador inyectando la API key. Se ejecuta una sola vez por clave."""
    import os
    os.environ["GEMINI_API_KEY"] = api_key
    # Forzar re-inicialización del cliente si ya estaba cargado
    import importlib, sys
    for mod in ["orchestrator", "config.settings", "config"]:
        if mod in sys.modules:
            del sys.modules[mod]
    import orchestrator as orc
    return orc


def _resolver_api_key() -> str | None:
    """Busca la API key en: variable de entorno → st.secrets → None."""
    import os
    # 1. Variable de entorno
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if key:
        return key
    # 2. Streamlit secrets (.streamlit/secrets.toml)
    try:
        key = st.secrets.get("GEMINI_API_KEY", "").strip()
        if key:
            return key
    except Exception:
        pass
    return None


# ── Resolver API key ──────────────────────────────────────────────────────────
if "api_key_confirmed" not in st.session_state:
    st.session_state.api_key_confirmed = False
if "api_key_value" not in st.session_state:
    st.session_state.api_key_value = ""

_auto_key = _resolver_api_key()
if _auto_key and not st.session_state.api_key_confirmed:
    st.session_state.api_key_value = _auto_key
    st.session_state.api_key_confirmed = True

# ── Cargar orquestador si hay clave ───────────────────────────────────────────
orc = None
sistema_ok = False
error_inicio = None

if st.session_state.api_key_confirmed and st.session_state.api_key_value:
    try:
        orc = _cargar_orquestador(st.session_state.api_key_value)
        sistema_ok = True
    except Exception as e:
        sistema_ok = False
        error_inicio = str(e)

# ─────────────────────────────────────────────────────────────────────────────
# Estado de sesión
# ─────────────────────────────────────────────────────────────────────────────

if "messages_ui" not in st.session_state:
    st.session_state.messages_ui = []       # historial para mostrar en UI
if "messages_orc" not in st.session_state:
    st.session_state.messages_orc = []      # historial interno para el orquestador
if "total_llamadas" not in st.session_state:
    st.session_state.total_llamadas = 0
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0
if "agente_actual" not in st.session_state:
    st.session_state.agente_actual = "Valeria"

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

AGENTE_CONFIG = {
    "Valeria": {"avatar": "🛍️", "rol": "Asesora Comercial Veltri"},
    "user":    {"avatar": "👤", "rol": "Cliente"},
}


# ─────────────────────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🖥️ Veltri Tecnologic")
    st.markdown("*Sistema Multiagente Swarm + MCP*")
    st.divider()

    # Asesora activa
    st.markdown(
        '<div class="agent-pill">🛍️ Valeria — Asesora Comercial</div>',
        unsafe_allow_html=True,
    )
    st.divider()

    st.markdown("**🏪 Veltri Tecnologic**")
    st.markdown("*Laptops · GPUs · CPUs · RAM · SSD*")
    st.markdown("*Fuentes · Monitores · Periféricos*")
    st.divider()

    # Métricas de sesión
    st.markdown("**📊 Métricas de sesión**")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Mensajes", len([m for m in st.session_state.messages_ui if m["role"] == "user"]))
    with col2:
        st.metric("Llamadas API", st.session_state.total_llamadas)

    st.divider()

    # Botón de reset
    if st.button("🔄 Nueva conversación", use_container_width=True):
        st.session_state.messages_ui = []
        st.session_state.messages_orc = []
        st.session_state.total_llamadas = 0
        st.session_state.total_tokens = 0
        st.session_state.agente_actual = "Valeria"
        st.rerun()

    st.markdown("")
    st.markdown(
        "<small style='color:#4b5563'>Modelo: gemini-2.5-flash<br>Protocolo: MCP + Swarm</small>",
        unsafe_allow_html=True,
    )

    # Cambiar API key
    st.divider()
    if st.button("🔑 Cambiar API Key", use_container_width=True):
        st.session_state.api_key_confirmed = False
        st.session_state.api_key_value = ""
        st.session_state.messages_ui = []
        st.session_state.messages_orc = []
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# Área principal
# ─────────────────────────────────────────────────────────────────────────────

# Header
st.markdown("""
<div class="veltri-header">
    <h1>🖥️ Veltri Tecnologic</h1>
    <p>Tu asesor inteligente de hardware — Powered by Gemini + Swarm MCP</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Pantalla de configuración de API key (si no hay clave) ──────────────────
if not st.session_state.api_key_confirmed:
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        st.markdown("""
        <div style="text-align:center; padding: 20px 0 10px;">
            <span style="font-size:3rem;">🔑</span>
            <h3 style="color:#c4b5fd; font-family:'Space Grotesk',sans-serif; margin:10px 0 4px;">Configura tu API Key</h3>
            <p style="color:#9ca3af; font-size:0.9rem;">Necesitas una clave de Google Gemini para iniciar el asistente.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form(key="api_key_form"):
            api_key_input = st.text_input(
                "GEMINI_API_KEY",
                type="password",
                placeholder="AIzaSy...",
                help="Obtén tu clave gratuita en https://aistudio.google.com/app/apikey",
            )
            submitted = st.form_submit_button("🚀 Iniciar asistente", use_container_width=True)

        if submitted:
            if api_key_input.strip():
                st.session_state.api_key_value = api_key_input.strip()
                st.session_state.api_key_confirmed = True
                with st.spinner("🔧 Inicializando sistema multiagente... esto puede tardar unos segundos."):
                    time.sleep(1)  # Brief feedback while loading
                st.rerun()
            else:
                st.warning("⚠️ Ingresa una clave válida antes de continuar.")

        st.markdown("""
        <div style="margin-top:16px; padding:12px 16px; background:rgba(124,58,237,0.08);
                    border:1px solid rgba(124,58,237,0.25); border-radius:10px; font-size:0.82rem; color:#9ca3af;">
            <strong style="color:#c4b5fd;">💡 Alternativa permanente:</strong><br>
            Crea el archivo <code>.streamlit/secrets.toml</code> con:
            <pre style="margin:6px 0 0; color:#e2e8f0;">GEMINI_API_KEY = "tu_clave_aqui"</pre>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

# ── Error al cargar el orquestador (clave inválida u otro problema) ─────────
if not sistema_ok:
    st.error(f"❌ Error al iniciar el sistema: {error_inicio}")
    if st.button("Cambiar API Key"):
        st.session_state.api_key_confirmed = False
        st.session_state.api_key_value = ""
        st.rerun()
    st.stop()

# Mensaje de bienvenida si no hay historial
if not st.session_state.messages_ui:
    with st.chat_message("assistant", avatar="🛍️"):
        st.markdown(
            "¡Hola! Soy **Valeria**, tu asesora personal de hardware en Veltri Tecnologic. 😊\n\n"
            "Cuéntame qué tipo de PC quieres armar o qué componente estás buscando. "
            "Si necesito ayuda de un especialista, lo traigo al chat automáticamente.\n\n"
            "**¿En qué te puedo ayudar hoy?**"
        )

# Renderizar historial de la conversación
for msg in st.session_state.messages_ui:
    role    = msg["role"]
    content = msg["content"]
    agent   = msg.get("agent", "Valeria")

    if role == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(content)
    else:
        with st.chat_message("assistant", avatar="🛍️"):
            st.markdown(f"**Valeria** · *Asesora Comercial Veltri*")
            st.markdown(content)

# ─────────────────────────────────────────────────────────────────────────────
# Input del usuario y procesamiento
# ─────────────────────────────────────────────────────────────────────────────

prompt = st.chat_input("Escribe tu consulta sobre hardware, precios o stock...")

if prompt:
    # 1. Mostrar mensaje del usuario inmediatamente
    st.session_state.messages_ui.append({"role": "user", "content": prompt, "agent": "user"})
    
    # Renderizar el mensaje del usuario
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # 2. Llamar al orquestador con spinner
    with st.spinner("✨ Valeria está preparando tu respuesta..."):
        try:
            resultado = orc.procesar_mensaje(prompt, st.session_state.messages_orc)
            error_msg = None
        except Exception as e:
            resultado = None
            error_msg = str(e)

    if error_msg:
        st.error(f"❌ Error al procesar el mensaje: `{error_msg}`")
    else:
        reply = resultado["reply"]

        # 3. Guardar y mostrar respuesta de Valeria
        st.session_state.messages_orc.append({"role": "user", "content": prompt})
        st.session_state.messages_orc.append({"role": "assistant", "content": reply})
        st.session_state.messages_ui.append({"role": "assistant", "content": reply})
        st.session_state.total_llamadas += 1

        # Renderizar la respuesta con efecto visual
        with st.chat_message("assistant", avatar="🛍️"):
            st.markdown("**Valeria** · *Asesora Comercial Veltri*")
            st.markdown(reply)
        
        # Hacer scroll hacia abajo y permitir que se actualice
        time.sleep(0.3)
    
    st.rerun()
