from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .crud import create_item, get_items
from . import schemas
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items", response_model=list[schemas.Item])
def get_all_items(db: Session = Depends(get_db)):
    """Returns list of all items"""

    items = get_items(db=db)
    return items

@app.post("/items", response_model=schemas.Item)
def add_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """Creates a new item"""

    new_item = create_item(item=item, db=db)
    return new_item
