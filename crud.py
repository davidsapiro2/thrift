from sqlalchemy.orm import Session
from . import models
from . import schemas

def get_all(db: Session, model: models):
    return db.query(model).all().sort()

def get_one(db: Session, model: models, id: int):
    return db.query(model).filter(model.id == id).first()

def create(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.model_dump()) # turns dict into a model instance
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update(db: Session, id: int, model: models, data: schemas):
    db_item = db.query(model).filter(model.id == id).first()

    if db_item is None:
        return None

    db_item = {
        "item": data.name,
        "description": data.description,
        "measurements": data.measurements
    }

    db.commit()
    db.refresh(db_item)
    return db_item
