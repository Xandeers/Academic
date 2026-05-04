from fastapi import APIRouter, HTTPException, Response

from schema.customer import (
    CreateCustomer,
    ResponseCustomer,
    UpdateCustomer
)
from model.customer import CustomerDB
from service.customer import create_customer_password, delete_customer_db, update_customer_db
from core.dependencies import CustomerDependency, SessionDependency

import logging

logger = logging.getLogger("uvicorn.error")

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)

@router.get("/", response_model=list[ResponseCustomer])
async def get_customers(db: SessionDependency):
    customers = db.query(CustomerDB).all()
    return customers

@router.get("/{customer_id}", response_model=ResponseCustomer)
async def get_customer(customer_id: int, db: SessionDependency) -> ResponseCustomer:
    """Route to get a customer by ID.

    Args:
        customer_id (int): The ID of the customer to retrieve
        db (SessionDependency): The database session

    Returns:
        CustomerSchema: The retrieved customer object
    """
    customer = db.query(CustomerDB).filter(CustomerDB.id_customer == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.post("/", response_model=ResponseCustomer)
async def create_customer(customer: CreateCustomer, db: SessionDependency) -> ResponseCustomer:
    """Route to create a customer.

        Args:
            customer (CreateCustomer): The customer data for creation
            db (SessionDependency): The database session

        Returns:
            CustomerSchema: The created customer object
        """
    logger.info(f"Creating customer with email: {customer.email}")

    new_customer = None
    if customer.auth_type == 'password':
        new_customer = create_customer_password(
            username= customer.username,
            firstname= customer.firstname,
            lastname= customer.lastname,
            email= customer.email,
            description= customer.description,
            password= customer.token,
            db= db
        )
    if customer.auth_type == 'google':
        raise HTTPException(status_code=400, detail="Google authentication not implemented yet")
    if customer.auth_type == 'facebook':
        raise HTTPException(status_code=400, detail="Facebook authentication not implemented yet")
    if new_customer is None:
        raise HTTPException(status_code=500, detail="failed to create a user")
    return new_customer

@router.put("/")
async def update_customer(new_customer: UpdateCustomer, customer: CustomerDependency, db: SessionDependency):
    update_customer_db(new_customer= new_customer, customer_id= customer.id_user, db= db)
    return Response(status_code=200, content="Update success")
    
@router.delete("/{customer_id}")
async def delete_customer(customer_id : int, db: SessionDependency):
    delete_customer_db(customer_id, db)
    return Response(status_code=200, content="Delete success")