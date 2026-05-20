import time
import google.generativeai as genai
from config.settings import MODELO, MAX_REINTENTOS, ESPERA_REINTENTO
from core.agent import Agent
from core.metrics import MetricsTracker

def run_swarm_gemini(agent: Agent, messages: list, metrics_tracker: MetricsTracker, event_bus=None) -> tuple:
    """
    Ejecuta una consulta al modelo Gemini usando el agente activo.
    Implementa reintentos automaticos con backoff para errores 429.
    Notifica a través de un EventBus si se proporciona.
    Retorna (agente_activo, respuesta_texto).
    """
    if event_bus:
        event_bus.publish("llamada_gemini_iniciada", {"agente": agent.name, "total_mensajes": len(messages)})

    # Construir historial compatible con Gemini
    gemini_history = []
    for msg in messages:
        role = "user" if msg["role"] == "user" else "model"
        gemini_history.append({"role": role, "parts": [msg["content"]]})

    # Crear modelo con instrucciones del agente
    model = genai.GenerativeModel(
        model_name=MODELO,
        system_instruction=agent.instructions
    )

    # Reintentos con backoff exponencial
    for intento in range(1, MAX_REINTENTOS + 1):
        print(f"  -> [Motor Swarm]: Llamando a {MODELO} como [{agent.name}] (intento {intento})...", flush=True)
        t0 = time.time()
        try:
            response = model.generate_content(
                gemini_history,
                request_options={"timeout": 30}
            )
            t1 = time.time()
            latencia = t1 - t0

            # Capturar Metricas Cuantitativas
            tokens = None
            try:
                tokens = response.usage_metadata.total_token_count
            except Exception:
                pass

            metrics_tracker.registrar_llamada(tokens, latencia)

            print(f"  -> [Metrica] Latencia: {latencia:.2f}s | Intento: {intento}/{MAX_REINTENTOS}")

            # Extraer texto de respuesta
            try:
                texto = response.text
            except (ValueError, AttributeError):
                texto = "[SISTEMA: El modelo no genero una respuesta de texto valida]"

            if event_bus:
                event_bus.publish("llamada_gemini_exito", {"agente": agent.name, "tokens": tokens, "latencia": latencia})

            return agent, texto

        except Exception as e:
            t1 = time.time()
            error_str = str(e)

            if event_bus:
                event_bus.publish("llamada_gemini_error", {"agente": agent.name, "error": error_str, "intento": intento})

            if "429" in error_str and intento < MAX_REINTENTOS:
                espera = ESPERA_REINTENTO * intento
                print(f"  -> [REINTENTO] Error 429 (cuota). Esperando {espera}s antes del intento {intento+1}...")
                time.sleep(espera)
            else:
                print(f"  -> [ERROR] Fallo en la llamada a Gemini (intento {intento}): {type(e).__name__}")
                if intento == MAX_REINTENTOS:
                    return agent, f"[SISTEMA: Error tras {MAX_REINTENTOS} intentos - {type(e).__name__}: cuota de API agotada. Espera unos minutos y reintenta.]"
