from sqlalchemy import Column, Integer, String, Numeric, Boolean, Text, TIMESTAMP
from database import Base

class Plant(Base):
    __tablename__ = "plants"
    id = Column(Integer, primary_key=True)
    slug = Column(String, unique=True, nullable=False)
    latin_name = Column(String)
    common_name_sv = Column(String)
    common_name_en = Column(String)
    plant_type = Column(String)
    hardiness_zone = Column(String)
    sun_req = Column(String)
    bloom_months = Column(String)
    height_cm_min = Column(Integer)
    height_cm_max = Column(Integer)
    description_sv = Column(Text)
    image_url = Column(String)

class Retailer(Base):
    __tablename__ = "retailers"
    id = Column(Integer, primary_key=True)
    slug = Column(String, unique=True)
    name = Column(String)
    url = Column(String)
    logo_url = Column(String)
    affiliate_id = Column(String)
    is_active = Column(Boolean)

class Listing(Base):
    __tablename__ = "listings"
    id = Column(Integer, primary_key=True)
    plant_id = Column(Integer)
    retailer_id = Column(Integer)
    price_sek = Column(Numeric)
    quantity = Column(Integer)
    unit_type = Column(String)
    price_per_unit = Column(Numeric)
    product_url = Column(String)
    in_stock = Column(Boolean)
    last_updated = Column(TIMESTAMP)
