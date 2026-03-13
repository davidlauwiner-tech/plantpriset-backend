from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import Plant, Listing, Retailer

router = APIRouter(prefix="/plants", tags=["plants"])

@router.get("")
def list_plants(plant_type: str = None, page: int = 1, limit: int = 20, db: Session = Depends(get_db)):
    q = db.query(Plant)
    if plant_type:
        q = q.filter(Plant.plant_type == plant_type)
    total = q.count()
    plants = q.offset((page - 1) * limit).limit(limit).all()
    result = []
    for p in plants:
        lowest = db.query(func.min(Listing.price_sek)).filter(
            Listing.plant_id == p.id, Listing.in_stock == True
        ).scalar()
        d = {c.name: getattr(p, c.name) for c in p.__table__.columns}
        d["lowest_price"] = float(lowest) if lowest else None
        result.append(d)
    return {"total": total, "page": page, "plants": result}

@router.get("/{slug}")
def get_plant(slug: str, db: Session = Depends(get_db)):
    plant = db.query(Plant).filter(Plant.slug == slug).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    listings_data = db.query(Listing, Retailer).join(
        Retailer, Listing.retailer_id == Retailer.id
    ).filter(Listing.plant_id == plant.id).order_by(Listing.price_sek).all()
    p = {c.name: getattr(plant, c.name) for c in plant.__table__.columns}
    p["listings"] = [
        {**{c.name: getattr(l, c.name) for c in l.__table__.columns},
         "retailer_name": r.name, "retailer_logo": r.logo_url}
        for l, r in listings_data
    ]
    return p
