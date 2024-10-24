from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import crud
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

    items = crud.get_items(db=db)
    return items

@app.get("/items/{item_id}", response_model=schemas.Item)
def get_one_item(item_id: int, db: Session = Depends(get_db)):
    """Returns details of one item"""

    item = crud.get_item(db=db, id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items", response_model=schemas.Item)
def add_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """Creates a new item"""

    new_item = crud.create_item(item=item, db=db)
    return new_item

@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item: schemas.Item, db: Session = Depends(get_db)):
    """Updates an item"""

    updated_item = crud.update_item(db=db, id=item_id, item=item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item