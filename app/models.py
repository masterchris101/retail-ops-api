from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class Worker(Base):
    __tablename__ = "workers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, default="OFA")
    shift = Column(String, default="day")  # day/night
    orders = relationship("Order", back_populates="worker")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="pending")  # pending/picked/packed/ready/cancelled
    channel = Column(String, default="pickup")  # pickup/delivery
    promised_minutes = Column(Integer, default=60)
    pick_time_minutes = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    worker_id = Column(Integer, ForeignKey("workers.id"), nullable=True)

    worker = relationship("Worker", back_populates="orders")

class InventoryItem(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    quantity = Column(Integer, default=0)
    location = Column(String, default="Aisle ?")
