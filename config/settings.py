"""
settings.py — Configuración centralizada del chatbot multiagente.

Variables globales, constantes de sistema y gestión de credenciales
para el cliente Gemini.
"""

import os
import sys
from typing import Optional

# ─────────────────────────────────────────────────────────────────────────────
# Configuración de modelo
# ─────────────────────────────────────────────────────────────────────────────

MODELO: str = 'gemini-1.5-flash'
"""Modelo de LLM utilizado para todas las llamadas."""

# ─────────────────────────────────────────────────────────────────────────────
# Configuración de reintentos
# ─────────────────────────────────────────────────────────────────────────────

MAX_REINTENTOS: int = 3
"""Número máximo de reintentos para llamadas a Gemini con error 429."""

ESPERA_REINTENTO: int = 30
"""Tiempo base en segundos para backoff exponencial en reintentos."""

# ─────────────────────────────────────────────────────────────────────────────
# Configuración de base de datos
# ─────────────────────────────────────────────────────────────────────────────

DB_PATH: str = "veltri_shop.db"
"""Ruta a la base de datos SQLite de productos."""

# ─────────────────────────────────────────────────────────────────────────────
# Configuración de sistema
# ─────────────────────────────────────────────────────────────────────────────

DEBUG_MODE: bool = os.environ.get("DEBUG", "false").lower() == "true"
"""Modo debug (activa logging verbose)."""

VERBOSE_LOGS: bool = os.environ.get("VERBOSE", "false").lower() == "true"
"""Modo verbose para salida en consola."""

# ─────────────────────────────────────────────────────────────────────────────
# Instancia global del cliente Gemini
# ─────────────────────────────────────────────────────────────────────────────

_client: Optional['genai.Client'] = None
"""Cliente Gemini singleton (inicializado al llamar configurar_gemini)."""

# ─────────────────────────────────────────────────────────────────────────────
# Forzar UTF-8 en Windows
# ─────────────────────────────────────────────────────────────────────────────

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def configurar_gemini() -> 'genai.Client':
    """Configura y retorna el cliente de Gemini.
    
    Lee la clave API desde la variable de entorno GEMINI_API_KEY
    y la utiliza para inicializar el cliente.
    
    Returns:
        Cliente Gemini configurado.
    
    Raises:
        ValueError: Si GEMINI_API_KEY no está configurada.
    """
    global _client
    
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError(
            "Error: Variable GEMINI_API_KEY no encontrada.\n\n"
            "Configúrala con uno de estos comandos:\n\n"
            "  PowerShell:  $env:GEMINI_API_KEY='tu_clave_aqui'\n"
            "  CMD:         set GEMINI_API_KEY=tu_clave_aqui\n\n"
            "Obtén tu clave en: https://aistudio.google.com/apikey"
        )
    
    import google.genai as genai
    _client = genai.Client(api_key=gemini_api_key)
    return _client


def get_client() -> 'genai.Client':
    """Retorna el cliente Gemini ya configurado.
    
    Returns:
        Cliente Gemini singleton.
    
    Raises:
        RuntimeError: Si el cliente no ha sido inicializado primero.
    """
    global _client
    if _client is None:
        raise RuntimeError(
            "Cliente Gemini no inicializado. "
            "Llama a configurar_gemini() primero."
        )
    return _client
