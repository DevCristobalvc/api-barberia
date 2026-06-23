-- BarberIA — Schema Supabase PostgreSQL
-- Ejecuta este SQL en el SQL Editor de tu proyecto Supabase

-- Habilitar extensión UUID
create extension if not exists "uuid-ossp";

-- SHOPS
create table if not exists shops (
  id          uuid primary key default uuid_generate_v4(),
  name        text not null,
  assistant_name text not null default 'SofIA',
  phone       text,
  address     text,
  timezone    text not null default 'America/Bogota',
  prompt      text,
  created_at  timestamptz not null default now()
);

-- BARBERS
create table if not exists barbers (
  id       uuid primary key default uuid_generate_v4(),
  shop_id  uuid not null references shops(id) on delete cascade,
  name     text not null,
  active   boolean not null default true
);

-- SERVICES
create table if not exists services (
  id       uuid primary key default uuid_generate_v4(),
  shop_id  uuid not null references shops(id) on delete cascade,
  name     text not null,
  duration int  not null,  -- minutos
  price    numeric(10,2) not null,
  active   boolean not null default true
);

-- BARBER_SERVICES (many-to-many)
create table if not exists barber_services (
  barber_id  uuid not null references barbers(id) on delete cascade,
  service_id uuid not null references services(id) on delete cascade,
  primary key (barber_id, service_id)
);

-- BARBER_SCHEDULES
create table if not exists barber_schedules (
  id         uuid primary key default uuid_generate_v4(),
  barber_id  uuid not null references barbers(id) on delete cascade,
  weekday    int  not null check (weekday between 0 and 6), -- 0=Lunes
  start_time time not null,
  end_time   time not null
);

-- BLOCKED_SLOTS
create table if not exists blocked_slots (
  id             uuid primary key default uuid_generate_v4(),
  barber_id      uuid not null references barbers(id) on delete cascade,
  start_datetime timestamptz not null,
  end_datetime   timestamptz not null,
  reason         text
);

-- CUSTOMERS
create table if not exists customers (
  id         uuid primary key default uuid_generate_v4(),
  shop_id    uuid not null references shops(id) on delete cascade,
  name       text not null,
  phone      text not null,
  notes      text,
  visits     int not null default 0,
  last_visit timestamptz,
  created_at timestamptz not null default now(),
  unique (shop_id, phone)
);

-- APPOINTMENTS
create table if not exists appointments (
  id             uuid primary key default uuid_generate_v4(),
  shop_id        uuid not null references shops(id) on delete cascade,
  barber_id      uuid not null references barbers(id),
  customer_id    uuid not null references customers(id),
  service_id     uuid not null references services(id),
  start_datetime timestamptz not null,
  end_datetime   timestamptz not null,
  status         text not null default 'pending'
                 check (status in ('pending','confirmed','completed','cancelled','no_show')),
  source         text not null default 'dashboard'
                 check (source in ('whatsapp','dashboard','api')),
  notes          text,
  created_at     timestamptz not null default now()
);

-- ÍNDICES
create index if not exists idx_appointments_shop_start on appointments(shop_id, start_datetime);
create index if not exists idx_appointments_barber on appointments(barber_id);
create index if not exists idx_customers_phone on customers(shop_id, phone);
create index if not exists idx_barbers_shop on barbers(shop_id);

-- ROW LEVEL SECURITY (básico — ajustar según auth de Supabase)
alter table shops enable row level security;
alter table barbers enable row level security;
alter table services enable row level security;
alter table customers enable row level security;
alter table appointments enable row level security;

-- Políticas de lectura pública para el MVP (restringir en producción)
create policy "public read shops" on shops for select using (true);
create policy "public read barbers" on barbers for select using (true);
create policy "public read services" on services for select using (true);
create policy "public read customers" on customers for select using (true);
create policy "public read appointments" on appointments for select using (true);
create policy "public write appointments" on appointments for all using (true);
create policy "public write customers" on customers for all using (true);

-- DATOS DE PRUEBA
insert into shops (id, name, assistant_name, phone, address)
values ('00000000-0000-0000-0000-000000000001', 'BarberIA Demo', 'SofIA', '+57 300 123 4567', 'Calle 93 #15-32, Bogotá')
on conflict do nothing;

insert into barbers (id, shop_id, name) values
  ('10000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000001', 'Carlos Mendoza'),
  ('10000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000001', 'Miguel Torres'),
  ('10000000-0000-0000-0000-000000000003', '00000000-0000-0000-0000-000000000001', 'Roberto Silva')
on conflict do nothing;

insert into services (id, shop_id, name, duration, price) values
  ('20000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000001', 'Corte Clásico', 30, 15000),
  ('20000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000001', 'Fade Americano', 45, 20000),
  ('20000000-0000-0000-0000-000000000003', '00000000-0000-0000-0000-000000000001', 'Corte + Barba', 60, 28000),
  ('20000000-0000-0000-0000-000000000004', '00000000-0000-0000-0000-000000000001', 'Afeitado Clásico', 30, 12000),
  ('20000000-0000-0000-0000-000000000005', '00000000-0000-0000-0000-000000000001', 'Diseño de Barba', 20, 10000)
on conflict do nothing;

-- Horarios: Lun-Sab 9:00-20:00
insert into barber_schedules (barber_id, weekday, start_time, end_time)
select barber_id, weekday, '09:00', '20:00'
from (
  values
    ('10000000-0000-0000-0000-000000000001'::uuid, 0),
    ('10000000-0000-0000-0000-000000000001', 1),
    ('10000000-0000-0000-0000-000000000001', 2),
    ('10000000-0000-0000-0000-000000000001', 3),
    ('10000000-0000-0000-0000-000000000001', 4),
    ('10000000-0000-0000-0000-000000000001', 5),
    ('10000000-0000-0000-0000-000000000002', 0),
    ('10000000-0000-0000-0000-000000000002', 1),
    ('10000000-0000-0000-0000-000000000002', 2),
    ('10000000-0000-0000-0000-000000000002', 3),
    ('10000000-0000-0000-0000-000000000002', 4),
    ('10000000-0000-0000-0000-000000000003', 1),
    ('10000000-0000-0000-0000-000000000003', 2),
    ('10000000-0000-0000-0000-000000000003', 3),
    ('10000000-0000-0000-0000-000000000003', 4),
    ('10000000-0000-0000-0000-000000000003', 5)
) as t(barber_id, weekday)
on conflict do nothing;
