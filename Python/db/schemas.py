from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    product: str
    quantity: int

class OrderCreate(BaseModel):
    order_id: int
    customer: str
    items: List[Item]

class OrderResponse(BaseModel):
    order_id: int
    customer: str
    items: List[Item]

    class Config:
        from_attributes = True
