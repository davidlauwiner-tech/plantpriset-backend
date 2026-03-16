from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import httpx

app = FastAPI(title="Plantpriset API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

def headers():
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/plants")
async def list_plants(plant_type: str = None, page: int = 1, limit: int = 20):
    params = {"limit": limit, "offset": (page - 1) * limit, "order": "common_name_sv"}
    if plant_type:
        params["plant_type"] = f"eq.{plant_type}"
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{SUPABASE_URL}/rest/v1/plants", headers=headers(), params=params)
    return {"plants": r.json(), "page": page}

@app.get("/plants/{slug}")
async def get_plant(slug: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{SUPABASE_URL}/rest/v1/plants?slug=eq.{slug}", headers=headers())
        plants = r.json()
        if not plants:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Plant not found")
        plant = plants[0]
        listings_r = await client.get(
            f"{SUPABASE_URL}/rest/v1/listings?plant_id=eq.{plant['id']}&select=*,retailers(*)",
            headers=headers()
        )
        plant["listings"] = listings_r.json()
    return plant

@app.get("/search")
async def search_plants(q: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{SUPABASE_URL}/rest/v1/plants?or=(common_name_sv.ilike.*{q}*,latin_name.ilike.*{q}*)",
            headers=headers()
        )
    return {"query": q, "results": r.json()}
