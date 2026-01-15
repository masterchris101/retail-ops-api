from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from . import models

def create_worker(db: Session, name: str, role: str, shift: str):
    w = models.Worker(name=name, role=role, shift=shift)
    db.add(w)
    db.commit()
    db.refresh(w)
    return w

def list_workers(db: Session):
    return db.query(models.Worker).all()

def get_worker(db: Session, worker_id: int):
    return db.query(models.Worker).filter(models.Worker.id == worker_id).first()

def create_order(db: Session, channel: str, promised_minutes: int, worker_id: int | None):
    o = models.Order(channel=channel, promised_minutes=promised_minutes, worker_id=worker_id)
    db.add(o)
    db.commit()
    db.refresh(o)
    return o

def list_orders(db: Session, status: str | None = None):
    q = db.query(models.Order)
    if status:
        q = q.filter(models.Order.status == status)
    return q.order_by(models.Order.created_at.desc()).all()

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def update_order(db: Session, order: models.Order, **fields):
    for k, v in fields.items():
        if v is not None:
            setattr(order, k, v)
    db.commit()
    db.refresh(order)
    return order

def create_item(db: Session, sku: str, name: str, quantity: int, location: str):
    item = models.InventoryItem(sku=sku, name=name, quantity=quantity, location=location)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def list_items(db: Session):
    return db.query(models.InventoryItem).order_by(models.InventoryItem.name.asc()).all()

def get_item(db: Session, item_id: int):
    return db.query(models.InventoryItem).filter(models.InventoryItem.id == item_id).first()

def update_item(db: Session, item: models.InventoryItem, **fields):
    for k, v in fields.items():
        if v is not None:
            setattr(item, k, v)
    db.commit()
    db.refresh(item)
    return item

def low_stock(db: Session, threshold: int):
    return db.query(models.InventoryItem).filter(models.InventoryItem.quantity <= threshold).all()

def kpis_today(db: Session):
    since = datetime.utcnow() - timedelta(hours=24)

    total = db.query(func.count(models.Order.id)).filter(models.Order.created_at >= since).scalar() or 0
    completed = db.query(func.count(models.Order.id)).filter(
        models.Order.created_at >= since,
        models.Order.status.in_(["ready", "packed", "picked"])
    ).scalar() or 0

    on_time = db.query(func.count(models.Order.id)).filter(
        models.Order.created_at >= since,
        models.Order.pick_time_minutes.isnot(None),
        models.Order.pick_time_minutes <= models.Order.promised_minutes
    ).scalar() or 0

    avg_pick = db.query(func.avg(models.Order.pick_time_minutes)).filter(
        models.Order.created_at >= since,
        models.Order.pick_time_minutes.isnot(None)
    ).scalar()

    return {
        "orders_last_24h": total,
        "completed_last_24h": completed,
        "on_time_last_24h": on_time,
        "on_time_rate": (on_time / total) if total else 0.0,
        "avg_pick_time_minutes": float(avg_pick) if avg_pick is not None else None
    }

def worker_performance(db: Session, worker_id: int):
    total = db.query(func.count(models.Order.id)).filter(models.Order.worker_id == worker_id).scalar() or 0
    avg_pick = db.query(func.avg(models.Order.pick_time_minutes)).filter(
        models.Order.worker_id == worker_id,
        models.Order.pick_time_minutes.isnot(None)
    ).scalar()
    on_time = db.query(func.count(models.Order.id)).filter(
        models.Order.worker_id == worker_id,
        models.Order.pick_time_minutes.isnot(None),
        models.Order.pick_time_minutes <= models.Order.promised_minutes
    ).scalar() or 0

    return {
        "worker_id": worker_id,
        "orders_assigned": total,
        "on_time_orders": on_time,
        "on_time_rate": (on_time / total) if total else 0.0,
        "avg_pick_time_minutes": float(avg_pick) if avg_pick is not None else None
    }
