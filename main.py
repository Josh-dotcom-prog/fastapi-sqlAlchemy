from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, item
from crud import get_item, create_item

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to create an item
@app.post("/items/")
async def create_item_endpoint(name: str, description: str, price: int, db: Session = Depends(get_db)):
    return create_item(db, name, description, price)


# Endpoint to get an item by ID
@app.get("/items/{item_id}")
async def get_item_endpoint(item_id: int, db: Session = Depends(get_db)):
    item = get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="item not found")
    return item

# Endpoint to get all items
@app.put("/items/{item_id}")
async def update_item_endpoint(item_id: int, name: str, description: str, price: int, db: Session = Depends(get_db)):
    item = db.query(item).filter(item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="item not found")
    
    item.name = name
    item.description = description
    item.price = price
    db.commit()
    db.refresh(item)
    
    return item

# Endpoint to delete an item
@app.delete("/items/{item_id}")
def delete_item_endpoint(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    return {"detail": "Item deleted"}