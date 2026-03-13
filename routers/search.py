from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from database import get_db
from models import Plant, Listing

router = APIRouter(prefix="/search", tags=["search"])

@router.get("")
def search_plants(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    term = f"%{q.lower()}%"
    plants = db.query(Plant).filter(
        or_(
            func.lower(Plant.common_name_sv).like(term),
            func.lower(Plant.latin_name).like(term),
            func.lower(Plant.common_name_en).like(term),
        )
    ).limit(20).all()
    result = []
    for p in plants:
        lowest = db.query(func.min(Listing.price_sek)).filter(
            Listing.plant_id == p.id, Listing.in_stock == True
        ).scalar()
        d = {c.name: getattr(p, c.name) for c in p.__table__.columns}
        d["lowest_price"] = float(lowest) if lowest else None
        result.append(d)
    return {"query": q, "results": result}
