from sqlalchemy.orm import Session
from . import models
from . import schemas

def get_all(db: Session, model: models):
    return db.query(model).all().sort()

def get_one(db: Session, model: models, id: int):
    return db.query(model).filter(model.id == id).first()

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
