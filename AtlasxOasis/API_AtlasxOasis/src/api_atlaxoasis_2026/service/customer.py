from schema.customer import UpdateCustomer
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional
from model.customer import CustomerDB
from model.user import UserDB
from model.authentication  import AuthenticationDB
from security.hashing import hash_password
import logging

logger = logging.getLogger("uvicorn.error")


def create_customer_password(
        username: Optional[str],
        firstname: str,
        lastname:str,
        email:str,
        description: Optional[str],
        password: str, 
        db: Session
    ) -> CustomerDB:
    """Create a customer with password authentication.

    Args:
        username (str): username of the customer
        firstname (str): firstname of the customer
        lastname (str): lastname of the customer
        email (str): email of the customer
        description (Optional[str]): description of the customer
        password (str): password hash of the customer
        db (Session): database session

    Returns:
        CustomerDB: the created customer object
    """
    user = db.query(UserDB).filter((UserDB.email == email)).first()
    if user is not None:
        logger.warning(f"Attempt to create customer with existing email: {email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    new_customer = CustomerDB(
        type_user= 'customer',
        username= username,
        firstname= firstname,
        lastname = lastname,
        email= email,
        description= description
    )
    
    db.add(new_customer)
    db.flush()
    db.refresh(new_customer)

    hashed_pwd = hash_password(password)

    auth = AuthenticationDB(
        type_auth = 'password',
        id_user = new_customer.id_customer,
        token = hashed_pwd
    )
    db.add(auth)
    db.commit()
    db.refresh(auth)
    db.refresh(new_customer)
    return new_customer
    
def update_customer_db(new_customer: UpdateCustomer, customer_id: int ,db: Session):
    old_customer = db.query(CustomerDB).filter(CustomerDB.id_customer == customer_id).first()
    if not old_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    for key, value in new_customer.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(old_customer, key, value)
    db.commit()
    db.refresh(old_customer)
    return old_customer
    
def delete_customer_db(id_customer: int, db: Session):
    customer = db.query(CustomerDB).filter(CustomerDB.id_customer == id_customer).first()
    db.delete(customer)
    db.commit()
    
    
