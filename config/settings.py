import os
import sys
import google.genai as genai

# Forzar UTF-8 en la consola de Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Configuración de modelo
MODELO = 'gemini-1.5-flash'
MAX_REINTENTOS = 3
ESPERA_REINTENTO = 30  # segundos

# Instancia global del cliente genai
_client = None

def configurar_gemini():
    """Configura y retorna el cliente de Gemini. Levanta ValueError si falta la API key."""
    global _client
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError(
            "Error: Variable GEMINI_API_KEY no encontrada.\n"
            "Configurala con:  $env:GEMINI_API_KEY='tu_clave'  (PowerShell)\n"
            "                  set GEMINI_API_KEY=tu_clave      (Windows CMD)"
        )
    _client = genai.Client(api_key=gemini_api_key)
    return _client

def get_client() -> genai.Client:
    """Retorna el cliente Gemini ya configurado."""
    global _client
    if _client is None:
        raise RuntimeError("Cliente Gemini no inicializado. Llama a configurar_gemini() primero.")
    return _client
