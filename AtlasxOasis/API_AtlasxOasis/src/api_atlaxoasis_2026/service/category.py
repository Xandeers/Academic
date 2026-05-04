from sqlalchemy.orm import Session

from model.category import CategoryDB

def create_category_db(label : str, db: Session) -> CategoryDB:
    category = CategoryDB(
        label = label
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def delete_category_db(id_category: int, db: Session):
    category = db.query(CategoryDB).filter(CategoryDB.id_category == id_category).first()
    db.delete(category)
    db.commit()