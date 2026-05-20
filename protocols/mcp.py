import time
import json

# Protocolo MCP (Model Context Protocol)
# Estado compartido validado con esquema JSON

MCP_SCHEMA = {
    "campos_requeridos": ["protocolo_mcp", "version", "timestamp", "datos_sesion", "resolucion_conflictos"],
    "version_soportada": "1.0"
}

PALABRAS_CLAVE_TECNICAS = [
    "cuello de botella", "bottleneck", "watts", "voltaje", "fuente de poder",
    "compatibilidad", "transferir", "especialista", "soporte tecnico",
    "no puedo responder", "no estoy capacitado", "derivar", "escalar",
    "tecnico", "hardware avanzado", "overclock", "tdp", "pcie",
    "chipset", "bios", "firmware"
]

PALABRAS_CLAVE_INVENTARIO = [
    "tienen stock", "hay stock", "disponible", "disponibilidad", "garantia", "garantía",
    "marca", "marcas", "tienda", "almacen", "entrega", "despacho", "envian", "envió", "recojo"
]

def validar_payload_mcp(payload: dict) -> bool:
    """Valida que el payload MCP cumpla con el esquema definido."""
    for campo in MCP_SCHEMA["campos_requeridos"]:
        if campo not in payload:
            print(f"  [MCP ERROR] Campo requerido ausente: {campo}")
            return False
    if payload.get("version") != MCP_SCHEMA["version_soportada"]:
        print(f"  [MCP ERROR] Version no soportada: {payload.get('version')}")
        return False
    return True

def generar_payload_mcp(agente_origen: str, agente_destino: str, motivo: str, 
                        shared_memory_data: dict, historial_resumen: str = "") -> dict:
    """
    Genera el estado compartido MCP como payload JSON para la transferencia entre agentes.
    Integra la memoria compartida del sistema.
    """
    estado_compartido_mcp = {
        "protocolo_mcp": "Activo",
        "version": "1.0",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "datos_sesion": {
            "cliente_perfil": shared_memory_data.get("cliente_perfil", {}),
            "consulta_stock": shared_memory_data.get("consulta_stock", {}),
            "estado_conversacion": motivo,
            "historial_preservado": historial_resumen
        },
        "resolucion_conflictos": {
            "estrategia": "Priorizar_estabilidad_hardware",
            "fallback": "Consultar_catalogo_compatible",
            "timeout_segundos": 30,
            "conflictos_detectados": []
        },
        "metricas_transferencia": {
            "agente_origen": agente_origen,
            "agente_destino": agente_destino,
            "motivo_escalamiento": motivo
        }
    }
    return estado_compartido_mcp

def resolver_conflictos_mcp(payload: dict, verbose: bool = True) -> dict:
    """
    Algoritmo de resolución de conflictos de estado en el payload de transferencia.
    """
    datos_sesion = payload.get("datos_sesion", {})
    consulta_stock = datos_sesion.get("consulta_stock", {})
    conflictos = []

    # Regla de Consistencia 1: Garantía informada requiere producto de interés
    if consulta_stock.get("garantia_informada") and not consulta_stock.get("producto_interes"):
        conflictos.append("Garantía marcada como informada sin definir el producto de interés")
        consulta_stock["garantia_informada"] = False  # Corrección

    # Regla de Consistencia 2: Entrega coordinada requiere stock confirmado
    if consulta_stock.get("entrega_coordinada") and not consulta_stock.get("stock_confirmado"):
        conflictos.append("Entrega coordinada antes de confirmar stock")
        consulta_stock["entrega_coordinada"] = False  # Corrección

    # Regla de Consistencia 3: Si se habla de la RTX 4060 pero no está registrada
    if not consulta_stock.get("producto_interes") and "4060" in str(datos_sesion):
        conflictos.append("Producto autodetectado (RTX 4060) a partir del historial")
        consulta_stock["producto_interes"] = "RTX 4060"

    payload["resolucion_conflictos"]["conflictos_detectados"] = conflictos
    
    if conflictos and verbose:
        print(f"  [MCP CONFLICT RESOLUTION] Conflictos detectados y resueltos: {conflictos}")
        
    return payload

def mostrar_transferencia_mcp(payload: dict, verbose: bool = True) -> bool:
    """Muestra en consola el proceso de transferencia MCP con validacion y resolucion de conflictos."""
    es_valido = validar_payload_mcp(payload)

    if es_valido:
        # Resolver conflictos
        payload = resolver_conflictos_mcp(payload, verbose)

    if verbose:
        print("\n" + "=" * 65)
        print("  [Sistema MCP]: Iniciando transferencia jerarquica...")
        print("  [Sistema MCP]: Validando payload contra esquema MCP...")
        estado = "VALIDADO" if es_valido else "ERROR DE VALIDACION"
        print(f"  [Sistema MCP]: Estado del payload preliminar: {estado}")
        print("  [Sistema MCP]: Payload JSON final transmitido:")
        print("=" * 65)
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        print("=" * 65)
        if es_valido:
            print("  [Sistema MCP]: Estado compartido transferido con exito.")
        else:
            print("  [Sistema MCP]: ADVERTENCIA - Transferencia con errores en estructura de datos.")
        print("=" * 65 + "\n")
    return es_valido

def necesita_escalamiento(respuesta: str) -> bool:
    """
    Determina si la respuesta o input indica que debe transferirse la conversacion
    al Especialista Técnico.
    """
    respuesta_lower = respuesta.lower()
    coincidencias = [p for p in PALABRAS_CLAVE_TECNICAS if p in respuesta_lower]
    if len(coincidencias) >= 2:
        return True
    frases_delegacion = [
        "transferir al especialista", "derivar al especialista", "soporte tecnico",
        "no estoy capacitado", "te paso con el especialista", "especialista tecnico"
    ]
    return any(f in respuesta_lower for f in frases_delegacion)

def necesita_inventario(respuesta: str) -> bool:
    """
    Determina si el flujo requiere transferirse al Asesor de Inventario.
    """
    respuesta_lower = respuesta.lower()
    coincidencias = [p for p in PALABRAS_CLAVE_INVENTARIO if p in respuesta_lower]
    if len(coincidencias) >= 2:
        return True
    frases_inventario = [
        "pasar al inventario", "agente de inventario", "validar stock", "tienen stock",
        "consultar stock", "recojo en tienda", "marcas disponibles", "politicas de garantia"
    ]
    return any(f in respuesta_lower for f in frases_inventario)
