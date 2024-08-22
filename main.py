from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .crud import create_item, get_items, get_item
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

@app.get("/items/{item_id}")
def get_one_item(item_id: int, db: Session = Depends(get_db)):
    """Returns details of one item"""

    item = get_item(item_id=item_id, db=db)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
