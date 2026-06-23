# Setup local — api-barberia

## Requisitos

- Python 3.12+
- Redis (opcional en desarrollo — la memoria de conversación falla sin él pero el resto funciona)
- Cuenta en [Supabase](https://supabase.com)

## 1. Clonar e instalar

```bash
git clone https://github.com/DevCristobalvc/api-barberia
cd api-barberia
python -m venv .venv

# Windows
.venv\Scripts\pip install -r requirements.txt

# macOS / Linux
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Configurar Supabase

1. Crear proyecto en [supabase.com](https://supabase.com)
2. Ir a **Settings → API** y copiar:
   - Project URL
   - `anon` public key
   - `service_role` secret key
3. Abrir **SQL Editor** y ejecutar el archivo `supabase_schema.sql`
   - Crea tablas, índices, RLS y datos de prueba

## 3. Variables de entorno

```bash
cp .env.example .env
```

```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-anon-key
SUPABASE_SERVICE_KEY=tu-service-role-key
OPENAI_API_KEY=sk-...
REDIS_URL=redis://localhost:6379   # opcional
```

## 4. Correr en desarrollo

```bash
uvicorn app.main:app --reload --port 8000
```

- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

## 5. Probar el agente

```bash
# Test rápido via curl
curl -X POST http://localhost:8000/api/v1/webhook/message/sync \
  -H "Content-Type: application/json" \
  -d '{
    "shop_id": "00000000-0000-0000-0000-000000000001",
    "phone": "+57300999888",
    "message": "Hola, quiero un corte"
  }'
```

## Redis (opcional en desarrollo)

Si no tienes Redis corriendo, los endpoints de webhook fallarán al intentar guardar conversación. Para desarrollo sin Redis, puedes comentar temporalmente el `await memory.append_message(...)` en `agent_service.py`.

Con Docker:
```bash
docker run -d -p 6379:6379 redis:7-alpine
```
