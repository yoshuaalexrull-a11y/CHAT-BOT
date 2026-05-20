# Sistema Multiagente MCP - Veltri Tecnologic (Asesor de Ventas y Soporte)

## Descripcion del Proyecto

Sistema de orquestacion multiagente basado en la arquitectura **Swarm** con delegacion jerarquica, desarrollado para **Veltri Tecnologic**. El sistema otorga una atencion personalizada a los clientes como un **chatbot asesor** (comercial, soporte técnico e inventario), permitiendo una atencion integral y eficiente. Utiliza el **Model Context Protocol (MCP)** para la comunicacion estructurada y validada entre agentes.

## Arquitectura del Sistema

### Diagrama de Arquitectura

```
+-------------------------------------------------------------+
|                     ORQUESTADOR (orchestrator.py)           |
|                                                             |
|   +-----------------------------------------------------+   |
|   |             Motor Swarm con Gemini (settings.py)    |   |
|   |   - Reintentos automaticos (backoff exponencial)    |   |
|   |   - Tracking de metricas y latencia (metrics.py)    |   |
|   |   - Historial conversacional preservado             |   |
|   +-----------------------------------------------------+   |
|                            |                                |
|            +---------------+---------------+                |
|            |               |               |                |
|   +--------v--------+ +----v----+ +--------v--------+       |
|   |  AGENTE VENTAS  | | TECNICO | |   INVENTARIO    |       |
|   |  (Sub-agente 1) | | (Sub-2) | |   (Sub-agente 3) |       |
|   |                 | |         | |                 |       |
|   | - Asesoría      | | - Cuello| | - Disponibilidad|       |
|   | - Presupuestos  | |   botella | - Garantías     |       |
|   | - Recomendación | | - Watts | | - Marcas        |       |
|   +-----------------+ +---------+ +-----------------+       |
|            ^               ^               ^                |
|            |               |               |                |
|            +---------------+---------------+                |
|                            | MCP JSON State                 |
|                            v                                |
|                    [Memoria Compartida]                     |
|                    [Bus de Eventos    ]                     |
+-------------------------------------------------------------+
```

### Topologia: Grafo de Agentes (Agent Graph)

Se define la topología de interacción mediante un grafo rígido que limita las delegaciones:
1. `agente_ventas` $\rightarrow$ `especialista_tecnico`: Cuando se detectan dudas sobre watts, overclocking o cuello de botella.
2. `agente_ventas` $\rightarrow$ `agente_inventario`: Cuando se indaga sobre stock disponible, marcas en tienda o políticas de garantía.
3. Ambos sub-agentes devuelven el control al `agente_ventas` una vez resuelta la consulta específica.

### Roles de los Agentes

| Agente | Responsabilidad | Cuando actúa |
|--------|----------------|--------------|
| `agente_ventas` | Atención comercial, presupuestos, recomendaciones de productos | Punto de entrada (predeterminado) |
| `especialista_tecnico` | Compatibilidad de hardware, voltajes, cuellos de botella, especificaciones | Escalamiento ante consultas técnicas avanzadas |
| `agente_inventario` | Disponibilidad física, marcas disponibles, garantías y tiempos de entrega | Escalamiento ante consultas de disponibilidad y logística |

---

## Componentes de la Arquitectura (Antigravity)

* **Grafo de Agentes (`core/agent_graph.py`)**: Define los nodos y las transiciones válidas.
* **Memoria Compartida (`core/memory.py`)**: Almacena variables de consulta (perfil de cliente, marcas, garantías) conservando el estado entre handoffs.
* **Bus de Eventos (`core/event_bus.py`)**: Utiliza el patrón Pub-Sub para reaccionar a eventos conversacionales (`mensaje_usuario`, `handoff_agente`, `stock_exitoso`).
* **Base de Datos SQLite (`core/database.py`)**: Gestiona la inicialización de `veltri_shop.db` e inyecta información real de stock, marcas y precios en las consultas del Asesor de Inventario.

---

## Protocolo MCP (Model Context Protocol)

La comunicación usa payloads JSON validados contra un esquema que incluye un algoritmo de **Resolución de Conflictos** (`resolver_conflictos_mcp`):

```json
{
  "protocolo_mcp": "Activo",
  "version": "1.0",
  "timestamp": "2026-05-20T04:30:12",
  "datos_sesion": {
    "cliente_perfil": {
      "presupuesto": 3500.0,
      "preferencias": ["Gaming"]
    },
    "consulta_stock": {
      "producto_interes": "RTX 4060",
      "marca_preferida": "ASUS",
      "stock_confirmado": true
    }
  },
  "resolucion_conflictos": {
    "estrategia": "Priorizar_estabilidad_hardware",
    "fallback": "Consultar_catalogo_compatible",
    "timeout_segundos": 30,
    "conflictos_detectados": []
  }
}
```

---

## Requisitos Previos

- **Python 3.10+**
- **pip** (gestor de paquetes de Python)
- **API Key de Google Gemini** (gratuita en [Google AI Studio](https://aistudio.google.com/apikey))

## Instalacion y Ejecución

### 1. Instalar dependencias
```bash
pip install google-generativeai pyyaml
```

### 2. Configurar la API Key (PowerShell / Windows CMD)
```powershell
$env:GEMINI_API_KEY="tu_api_key_aqui"
```
```cmd
set GEMINI_API_KEY=tu_api_key_aqui
```

### 3. Ejecutar el chatbot
```bash
python orchestrator.py
```

---

## Casos de Prueba Automatizados

| # | Caso | Entrada del Cliente | Objetivo del Test |
|---|------|---------------------|-------------------|
| 1 | Flujo comercial | Presupuesto y juegos de interés | Evaluar recomendación y guardado en memoria |
| 2 | Adversarial | Inyección de prompt (100% descuento) | Evaluar robustez ante manipulaciones de prompt |
| 3 | Handoff Técnico | Cuello de botella e i3 antiguo | Probar handoff MCP a especialista de soporte |
| 4 | Handoff Inventario | Stock disponible, marcas y garantía | Probar handoff MCP al asesor de almacén |
| 5 | Fuera de dominio | Ayuda con tarea de integrales | Evaluar filtrado de consultas externas |
