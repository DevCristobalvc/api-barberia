# Tools del agente

El agente dispone de 13 tools. El LLM decide cuál usar según el mensaje del cliente. Todas son testeables de forma independiente (ver [agent-barberia](https://github.com/DevCristobalvc/agent-barberia)).

## Disponibilidad

### `get_availability`
Consulta horarios libres para un servicio en una fecha.

```python
get_availability(
    shop_id="uuid",
    service_duration=30,    # minutos
    date_str="2025-06-24",  # YYYY-MM-DD
    barber_id="uuid"        # opcional
)
# → {"Carlos Mendoza": {"barber_id": "...", "slots": ["09:00", "11:30"]}}
```

Lógica: toma el horario del barbero, resta las citas existentes y slots bloqueados, y devuelve slots de 30 min disponibles.

## Citas

### `create_booking`
Crea una cita verificando conflictos antes de insertar.

### `cancel_booking`
Cancela una cita existente (cambia status a `cancelled`).

### `move_booking`
Reprograma una cita a otro horario, verificando disponibilidad.

### `list_today`
Lista todas las citas del día actual con joins a clientes, barberos y servicios.

## Clientes

### `search_customer`
Busca por teléfono. Retorna `None` si no existe (el agente crea uno nuevo).

### `create_customer`
Crea un nuevo cliente. Se llama automáticamente cuando el cliente no está registrado.

### `update_customer`
Actualiza nombre o notas de un cliente existente.

## Información del negocio

### `get_shop_information`
Retorna nombre, dirección, teléfono, horarios y prompt personalizado.

### `list_services`
Lista todos los servicios activos con duración y precio.

### `list_barbers`
Lista barberos activos con sus servicios disponibles.

### `block_schedule`
Bloquea un período (vacaciones, descanso). Usado desde el dashboard admin.

### `unblock_schedule`
Elimina un bloqueo de horario.

## Probar tools de forma aislada

```bash
# Desde agent-barberia/
python -m pytest tests/test_tools.py -v

# O conversar con el agente localmente
python test_agent_local.py
```
