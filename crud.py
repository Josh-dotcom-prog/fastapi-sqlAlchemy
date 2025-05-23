from sqlalchemy.orm import Session
from models import item

def get_item(db: Session, item_id: int):
    return db.query(item).filter(item.id == item_id).first()

def create_item(db:Session, name: str, description: str, price: int):
    db_item = item(name=name, description=description, price=price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item