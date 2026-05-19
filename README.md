# Sistema Multiagente MCP - Veltri Tecnologic

## Descripcion del Proyecto

Sistema de orquestacion multiagente basado en la arquitectura **Swarm** con delegacion jerarquica, desarrollado para **Veltri Tecnologic**. El sistema automatiza la atencion al cliente para venta de componentes de hardware (tarjetas graficas RTX 4060), utilizando el **Model Context Protocol (MCP)** para la comunicacion estructurada entre agentes.

## Arquitectura del Sistema

### Diagrama de Arquitectura

```
+----------------------------------------------------------+
|                    ORQUESTADOR (orchestrator.py)          |
|                                                          |
|   +--------------------------------------------------+   |
|   |              Motor Swarm con Gemini              |   |
|   |   - Reintentos automaticos (backoff exponencial) |   |
|   |   - Tracking de metricas por llamada             |   |
|   |   - Historial conversacional preservado          |   |
|   +--------------------------------------------------+   |
|                          |                               |
|            +-------------+-------------+                 |
|            |                           |                 |
|   +--------v--------+       +---------v---------+       |
|   |  AGENTE VENTAS  |       | ESPECIALISTA      |       |
|   |  (Sub-agente 1) |  MCP  | TECNICO           |       |
|   |                 +------>+ (Sub-agente 2)     |       |
|   | - Atencion      | JSON  |                   |       |
|   | - Presupuestos  | Schema| - Compatibilidad  |       |
|   | - Recomendacion | Valid.| - Rendimiento     |       |
|   +-----------------+       | - Especificaciones|       |
|                             +-------------------+       |
+----------------------------------------------------------+
                         |
              +----------v----------+
              |   Gemini 2.0 Flash  |
              |   (API de Google)   |
              +---------------------+
```

### Topologia: Delegacion Jerarquica (Swarm)

Se eligio la topologia **jerarquica tipo Swarm** porque:

1. **Flujo natural del dominio**: En una tienda de tecnologia, el vendedor atiende primero y escala al tecnico solo cuando es necesario.
2. **Eficiencia de recursos**: El especialista tecnico solo se activa bajo demanda, minimizando tokens consumidos.
3. **Separacion de responsabilidades**: Cada agente tiene un dominio claro sin solapamiento.

### Roles de los Agentes

| Agente | Responsabilidad | Cuando actua |
|--------|----------------|--------------|
| `agente_ventas` | Atencion comercial, presupuestos, recomendaciones de productos | Siempre (punto de entrada) |
| `especialista_tecnico` | Compatibilidad de hardware, voltajes, cuellos de botella, especificaciones | Solo por escalamiento via MCP |
| `orquestador` | Coordinacion, deteccion de escalamiento, metricas, transferencia MCP | Permanente (controla el flujo) |

## Protocolo MCP (Model Context Protocol)

La comunicacion entre agentes usa payloads JSON validados contra un esquema:

```json
{
  "protocolo_mcp": "Activo",
  "version": "1.0",
  "timestamp": "2026-05-16T16:58:36",
  "datos_sesion": {
    "perfil_cliente": "Extraido del contexto conversacional",
    "estado_conversacion": "Transferencia por duda tecnica",
    "datos_adicionales": "...",
    "historial_preservado": "..."
  },
  "resolucion_conflictos": {
    "estrategia": "Priorizar_estabilidad_hardware",
    "fallback": "Consultar_catalogo_compatible",
    "timeout_segundos": 30
  },
  "metricas_transferencia": {
    "agente_origen": "agente_ventas",
    "agente_destino": "especialista_tecnico",
    "motivo_escalamiento": "..."
  }
}
```

### Caracteristicas del MCP:
- **Validacion de esquema** antes de cada transferencia
- **Historial preservado** entre turnos y agentes
- **Resolucion de conflictos** con estrategia definida y fallback
- **Metricas de transferencia** integradas en el payload

## Requisitos Previos

- **Python 3.10+**
- **pip** (gestor de paquetes de Python)
- **API Key de Google Gemini** (gratuita en [Google AI Studio](https://aistudio.google.com/apikey))

## Instalacion Paso a Paso

### 1. Clonar o descargar el proyecto

```bash
git clone <url-del-repositorio>
cd Veltri_Multiagente
```

### 2. Instalar dependencias

```bash
pip install google-generativeai pyyaml
```

### 3. Configurar la API Key

**Windows PowerShell:**
```powershell
$env:GEMINI_API_KEY="tu_api_key_aqui"
```

**Windows CMD:**
```cmd
set GEMINI_API_KEY=tu_api_key_aqui
```

**Linux/macOS:**
```bash
export GEMINI_API_KEY="tu_api_key_aqui"
```

### 4. Ejecutar el orquestador

```bash
python orchestrator.py
```

## Estructura del Proyecto

```
Veltri_Multiagente/
|-- orchestrator.py      # Orquestador principal con motor Swarm
|-- subagents.yaml       # Configuracion de roles y directivas de agentes
|-- task_plan.md         # Plan de tareas del proceso TO-BE
|-- README.md            # Documentacion tecnica (este archivo)
```

## Casos de Prueba

| # | Caso | Descripcion | Objetivo |
|---|------|-------------|----------|
| 1 | Flujo normal | Cliente pide armar PC con presupuesto | Verificar embudo de ventas |
| 2 | Adversarial | Inyeccion de prompt pidiendo 100% descuento | Evaluar resistencia a manipulacion |
| 3 | Delegacion MCP | Pregunta tecnica sobre cuello de botella | Verificar handoff Swarm y MCP |
| 4 | Edge case | Consulta fuera de dominio (matematicas) | Verificar limites del agente |

## Metricas Reportadas

El sistema reporta automaticamente al finalizar:

- **Tiempo total de ejecucion** (segundos)
- **Tokens totales consumidos**
- **Llamadas totales al modelo**
- **Latencia promedio, minima y maxima** por llamada
- **Tasa de exito** (porcentaje de pruebas exitosas)
- **Resultado individual** por cada caso de prueba (PASS/FAIL)

## Tecnologias Utilizadas

- **Google Gemini 2.0 Flash** - Modelo de lenguaje para generacion de respuestas
- **Swarm (patron arquitectonico)** - Delegacion jerarquica entre agentes
- **MCP (Model Context Protocol)** - Comunicacion estructurada via JSON
- **Python 3.12** - Lenguaje de implementacion
- **YAML** - Configuracion declarativa de agentes
- **Claude Code / Antigravity** - Herramienta de desarrollo asistido por IA
