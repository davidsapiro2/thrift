from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .crud import create, get_all, get_one, update
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

#######################################################
#################### Items ############################
#######################################################

@app.get("/items", response_model=list[schemas.Item])
def get_all_items(db: Session = Depends(get_db)):
    """Returns list of all items"""

    items = get_all(db=db, model=models.Item)
    return items

@app.get("/items/{item_id}")
def get_one_item(item_id: int, db: Session = Depends(get_db)):
    """Returns details of one item"""

    item = get_one(db=db, model=models.Item, id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items", response_model=schemas.Item)
def add_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """Creates a new item"""

    new_item = create(item=item, db=db)
    return new_item

@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item: schemas.Item, db: Session = Depends(get_db)):
    """Updates an item"""

    updated_item = update(db=db, model=models.Item, id=item_id, data=item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item