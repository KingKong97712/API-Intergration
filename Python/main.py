import os
from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from db.database import SessionLocal, Order, OrderItem
from db.schemas import OrderCreate, OrderResponse
from typing import List,Dict
from dotenv import load_dotenv
# API_KEY Read from .env File
load_dotenv()
API_KEY = os.getenv("API_KEY")
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def validate_api_key(api_key: str = Header(...)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
#  Function to save an order
@app.post("/api/orders", response_model=dict)
def create_order(orders: List[OrderCreate], db: Session = Depends(get_db), api_key: str = Depends(validate_api_key)):
    order_ids = [] 
    warnings: Dict[int, str] = {}

    for order in orders:
        # Validate Input
        if not order.order_id or not order.customer or not isinstance(order.items, list) or len(order.items) == 0:
            raise HTTPException(status_code=400, detail="Invalid input data")
        # Check if the order ID already exists
        existing_order = db.query(Order).filter(Order.order_id == order.order_id).first()
        if existing_order:
            # Add a warning message with the order_id
            warnings[order.order_id] = f"Order ID {order.order_id} already exists."
            continue 

        db_order = Order(order_id=order.order_id, customer=order.customer)
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        
        for item in order.items:
            db_item = OrderItem(order_id=order.order_id, product=item.product, quantity=item.quantity)
            db.add(db_item)
        
        db.commit()
        order_ids.append(order.order_id)
    return {"status": "success", "order_ids": order_ids, "warnings": warnings}
# Function to get order details by order_id
@app.get("/api/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db), api_key: str = Depends(validate_api_key)):
    db_order = db.query(Order).filter(Order.order_id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    return {"order_id": db_order.order_id, "customer": db_order.customer, "items": items}
