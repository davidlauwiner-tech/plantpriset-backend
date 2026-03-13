from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import plants, search

app = FastAPI(title="Plantpriset API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plants.router)
app.include_router(search.router)

@app.get("/health")
def health():
    return {"status": "ok"}
