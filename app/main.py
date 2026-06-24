import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router

app = FastAPI(
    title="BarberIA API",
    description="Backend del agente IA para barberías",
    version="0.1.0",
)

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    # Vercel — dominios fijos
    "https://barberia-flax-chi.vercel.app",
    "https://crm-barberia-psi.vercel.app",
    "https://client-barberia.vercel.app",
    # Vercel — preview deployments (*.vercel.app)
    "https://crm-barberia-devcristobalvc.vercel.app",
    "https://client-barberia-devcristobalvc.vercel.app",
    # DevTunnels — se agrega via env var para no hardcodear la URL
]

# Permite agregar orígenes extra via env var (ej: EXTRA_ORIGINS=https://xxx.devtunnels.ms)
extra = os.environ.get("EXTRA_ORIGINS", "")
if extra:
    ALLOWED_ORIGINS.extend([o.strip() for o in extra.split(",") if o.strip()])

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_origin_regex=r"https://.*\.vercel\.app|https://.*\.devtunnels\.ms",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "barberia-api"}
