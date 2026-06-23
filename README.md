# api-barberia — Backend

Backend del sistema BarberIA. Expone la API REST y el agente de IA que gestiona citas mediante conversación en lenguaje natural.

## Stack

FastAPI 0.138 · Python 3.12 · LangGraph 1.2.6 · Supabase 2.31 · Redis · OpenAI

## Inicio rápido

```bash
git clone https://github.com/DevCristobalvc/api-barberia
cd api-barberia

python -m venv .venv
# Windows:
.venv\Scripts\pip install -r requirements.txt
# macOS/Linux:
source .venv/bin/activate && pip install -r requirements.txt

cp .env.example .env    # completar con credenciales Supabase
uvicorn app.main:app --reload --port 8000
# → http://localhost:8000/docs
```

## Endpoints principales

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/api/v1/webhook/message` | Recibe mensaje de WhatsApp (async) |
| `POST` | `/api/v1/webhook/message/sync` | Recibe mensaje y responde sync (testing) |
| `GET` | `/api/v1/appointments/{shop_id}` | Lista citas |
| `POST` | `/api/v1/appointments/` | Crea cita |
| `GET` | `/api/v1/clients/{shop_id}` | Lista clientes |
| `GET` | `/api/v1/barbers/{shop_id}` | Lista barberos |

Documentación interactiva completa en `/docs` (Swagger UI).

## Documentación

- [Setup y configuración](docs/setup.md)
- [Arquitectura del sistema](docs/architecture.md)
- [Referencia de la API](docs/api.md)
- [Tools del agente](docs/tools.md)

## Repos relacionados

- **Frontend + Dashboard**: [BarberIA](https://github.com/DevCristobalvc/BarberIA)
- **Tests del agente**: [agent-barberia](https://github.com/DevCristobalvc/agent-barberia)
