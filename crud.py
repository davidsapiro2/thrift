from sqlalchemy.orm import Session
#from fastapi.encoders import jsonable_encoder
from . import models
from . import schemas

def get_items(db: Session):
    return db.query(models.Item).all()

def get_item(db: Session, id: int):
    return db.query(models.Item).filter(models.Item.id == id).first()

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.model_dump()) # turns dict into a model instance
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, id: int, item: schemas.Item):
    db_item = db.query(models.Item).filter(models.Item.id == id).first()

    if db_item is None:
        return None

    # for key, value in item.model_dump(exclude_unset=True).items():
    #     setattr(db_item, key, value)

    db_item.name = item.name
    db_item.description = item.description
    db_item.measurements = item.measurements

    db.commit()
    db.refresh(db_item)
    return db_item
