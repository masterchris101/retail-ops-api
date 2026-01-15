from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WorkerCreate(BaseModel):
    name: str
    role: str = "OFA"
    shift: str = "day"

class WorkerOut(BaseModel):
    id: int
    name: str
    role: str
    shift: str
    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    channel: str = "pickup"
    promised_minutes: int = 60
    worker_id: Optional[int] = None

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    pick_time_minutes: Optional[int] = None
    worker_id: Optional[int] = None

class OrderOut(BaseModel):
    id: int
    status: str
    channel: str
    promised_minutes: int
    pick_time_minutes: Optional[int]
    created_at: datetime
    worker_id: Optional[int]
    class Config:
        from_attributes = True

class InventoryCreate(BaseModel):
    sku: str
    name: str
    quantity: int = 0
    location: str = "Aisle ?"

class InventoryUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[int] = None
    location: Optional[str] = None

class InventoryOut(BaseModel):
    id: int
    sku: str
    name: str
    quantity: int
    location: str
    class Config:
        from_attributes = True
