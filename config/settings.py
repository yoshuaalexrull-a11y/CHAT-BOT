import os
import sys
import google.generativeai as genai

# Forzar UTF-8 en la consola de Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Configuración de modelo
MODELO = 'gemini-2.5-flash'
MAX_REINTENTOS = 3
ESPERA_REINTENTO = 30  # segundos

# Cargar API Key
def configurar_gemini():
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError(
            "Error: Variable GEMINI_API_KEY no encontrada.\n"
            "Configurala con:  set GEMINI_API_KEY=tu_clave  (Windows CMD)\n"
            "                  $env:GEMINI_API_KEY='tu_clave'  (PowerShell)"
        )
    genai.configure(api_key=gemini_api_key)
