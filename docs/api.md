# Referencia de la API

Base URL: `http://localhost:8000` (dev) · Swagger UI: `/docs`

## Webhook (agente)

### `POST /api/v1/webhook/message`
Procesa un mensaje en background (para producción con WhatsApp).

```json
{
  "shop_id": "00000000-0000-0000-0000-000000000001",
  "phone": "+57300123456",
  "message": "Quiero un corte para mañana"
}
```
Respuesta: `{"status": "received"}`

### `POST /api/v1/webhook/message/sync`
Igual pero espera la respuesta del agente (para testing).

```json
// Response
{"response": "Claro ✂️ Tenemos a Carlos (10:00, 11:30)..."}
```

## Citas

### `GET /api/v1/appointments/{shop_id}`
Lista citas. Query params: `date_from`, `date_to` (ISO format).

### `GET /api/v1/appointments/{shop_id}/today`
Citas del día con joins a clientes, barberos y servicios.

### `POST /api/v1/appointments/`
```json
{
  "shop_id": "uuid",
  "barber_id": "uuid",
  "customer_id": "uuid",
  "service_id": "uuid",
  "start_datetime": "2025-06-24T09:00:00",
  "end_datetime": "2025-06-24T09:30:00"
}
```

### `PATCH /api/v1/appointments/{id}`
Actualiza status, horario o notas.

### `DELETE /api/v1/appointments/{id}`
Cancela la cita (cambia status a `cancelled`).

## Clientes

### `GET /api/v1/clients/{shop_id}?q=nombre`
Lista o busca clientes. El parámetro `q` busca en nombre, teléfono y notas.

### `POST /api/v1/clients/`
Crea cliente. `phone` es único por `shop_id`.

### `PATCH /api/v1/clients/{id}`
Actualiza nombre o notas.

## Barberos

### `GET /api/v1/barbers/{shop_id}`
Lista barberos activos. `?active_only=false` incluye inactivos.

### `GET /api/v1/barbers/{barber_id}/schedule`
Retorna el horario semanal del barbero.

### `POST /api/v1/barbers/`
Crea barbero.

### `PATCH /api/v1/barbers/{id}`
Actualiza nombre o status activo.

## Estados de cita

| Status | Descripción |
|---|---|
| `pending` | Recién creada |
| `confirmed` | Confirmada |
| `completed` | Atendida |
| `cancelled` | Cancelada |
| `no_show` | Cliente no asistió |
