# Arquitectura del sistema

## Flujo completo

```
Cliente WhatsApp
      │
      ▼
Evolution API / Baileys (webhook)
      │
      ▼
POST /api/v1/webhook/message
      │
      ▼
FastAPI → AgentService.process_message()
      │
      ├─ Carga contexto de Redis (historial de conversación)
      ├─ Carga datos del shop (Supabase)
      ├─ Construye system prompt dinámico
      │
      ▼
LangGraph StateGraph (ReAct loop)
      │
      ├─── agent node (ChatOpenAI gpt-4o-mini)
      │         │
      │    ¿tool_calls?
      │         ├─ SÍ → tools node → ejecuta tool → vuelve a agent
      │         └─ NO → END
      │
      ▼
Respuesta de texto
      │
      ├─ Guarda turno en Redis
      ▼
WhatsApp ← respuesta enviada por Evolution API
```

## Estructura del proyecto

```
app/
├── main.py                  # FastAPI app, CORS, routers
├── config/settings.py       # Pydantic Settings (.env)
├── api/v1/
│   ├── router.py            # Agrega todos los sub-routers
│   ├── webhook.py           # POST /webhook/message
│   ├── appointments.py      # CRUD de citas
│   ├── clients.py           # CRUD de clientes
│   └── barbers.py           # CRUD de barberos
├── agents/
│   └── assistant.py         # LangGraph StateGraph + tools binding
├── tools/                   # 13 tools del agente (ver tools.md)
│   ├── availability.py
│   ├── bookings.py
│   ├── customers.py
│   └── shop_info.py
├── services/
│   └── agent_service.py     # Orquesta: redis + supabase + langgraph
├── repositories/            # Acceso a Supabase, sin SQL directo
│   ├── appointment_repo.py
│   ├── customer_repo.py
│   ├── barber_repo.py
│   └── shop_repo.py
├── schemas/                 # Pydantic models (request/response)
│   ├── appointment.py
│   ├── customer.py
│   ├── barber.py
│   ├── service.py
│   ├── shop.py
│   └── message.py
├── database/supabase.py     # Singleton del cliente Supabase
├── memory/conversation.py   # Redis: historial de conversación
└── prompts/system_prompt.py # Construye prompt dinámico por shop
```

## Multi-tenant

Cada request lleva `shop_id`. El `AgentService` carga en runtime los datos específicos del negocio (servicios, barberos, prompt personalizado) para construir el system prompt. Una sola instancia de la API atiende múltiples barberías.

## Agente ReAct

El agente nunca inventa datos. Cada respuesta que requiere información (disponibilidad, servicios, clientes) pasa por una tool que consulta Supabase. El LLM solo razona y genera texto a partir de resultados reales.

```python
StateGraph(AgentState):
  START → agent → conditional:
    tool_calls present → tools → agent (loop)
    no tool_calls     → END
```

## Memoria de conversación

- **Store**: Redis con TTL de 6 horas
- **Key**: `conversation:{shop_id}:{phone}`
- **Ventana**: últimos 30 mensajes
- **Propósito**: el agente recuerda el servicio elegido, el nombre del cliente, preferencias del turno actual

## Base de datos

Ver `supabase_schema.sql` para el schema completo. Tablas principales:

| Tabla | Descripción |
|---|---|
| `shops` | Negocios (multi-tenant) |
| `barbers` | Barberos por negocio |
| `services` | Servicios y precios |
| `barber_schedules` | Horarios por día |
| `blocked_slots` | Vacaciones / bloqueos |
| `customers` | Clientes con historial |
| `appointments` | Citas (5 estados) |
