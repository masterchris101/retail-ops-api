import os
from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from .db import SessionLocal, engine, Base
from . import schemas, crud

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Retail Ops API", version="1.0.0")

API_KEY = os.getenv("API_KEY", "dev-key")

def require_api_key(x_api_key: str | None = Header(default=None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Workers ---
@app.post("/workers", response_model=schemas.WorkerOut, dependencies=[Depends(require_api_key)])
def create_worker(payload: schemas.WorkerCreate, db: Session = Depends(get_db)):
    return crud.create_worker(db, payload.name, payload.role, payload.shift)

@app.get("/workers", response_model=list[schemas.WorkerOut], dependencies=[Depends(require_api_key)])
def list_workers(db: Session = Depends(get_db)):
    return crud.list_workers(db)

@app.get("/workers/{worker_id}", response_model=schemas.WorkerOut, dependencies=[Depends(require_api_key)])
def get_worker(worker_id: int, db: Session = Depends(get_db)):
    w = crud.get_worker(db, worker_id)
    if not w:
        raise HTTPException(404, "Worker not found")
    return w

@app.get("/workers/{worker_id}/performance", dependencies=[Depends(require_api_key)])
def worker_perf(worker_id: int, db: Session = Depends(get_db)):
    w = crud.get_worker(db, worker_id)
    if not w:
        raise HTTPException(404, "Worker not found")
    return crud.worker_performance(db, worker_id)

# --- Orders ---
@app.post("/orders", response_model=schemas.OrderOut, dependencies=[Depends(require_api_key)])
def create_order(payload: schemas.OrderCreate, db: Session = Depends(get_db)):
    if payload.worker_id is not None and not crud.get_worker(db, payload.worker_id):
        raise HTTPException(400, "worker_id does not exist")
    return crud.create_order(db, payload.channel, payload.promised_minutes, payload.worker_id)

@app.get("/orders", response_model=list[schemas.OrderOut], dependencies=[Depends(require_api_key)])
def list_orders(status: str | None = None, db: Session = Depends(get_db)):
    return crud.list_orders(db, status=status)

@app.patch("/orders/{order_id}", response_model=schemas.OrderOut, dependencies=[Depends(require_api_key)])
def update_order(order_id: int, payload: schemas.OrderUpdate, db: Session = Depends(get_db)):
    o = crud.get_order(db, order_id)
    if not o:
        raise HTTPException(404, "Order not found")

    if payload.worker_id is not None and not crud.get_worker(db, payload.worker_id):
        raise HTTPException(400, "worker_id does not exist")

    return crud.update_order(
        db, o,
        status=payload.status,
        pick_time_minutes=payload.pick_time_minutes,
        worker_id=payload.worker_id
    )

# --- Inventory ---
@app.post("/inventory", response_model=schemas.InventoryOut, dependencies=[Depends(require_api_key)])
def create_item(payload: schemas.InventoryCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, payload.sku, payload.name, payload.quantity, payload.location)

@app.get("/inventory", response_model=list[schemas.InventoryOut], dependencies=[Depends(require_api_key)])
def list_items(db: Session = Depends(get_db)):
    return crud.list_items(db)

@app.patch("/inventory/{item_id}", response_model=schemas.InventoryOut, dependencies=[Depends(require_api_key)])
def update_item(item_id: int, payload: schemas.InventoryUpdate, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(404, "Item not found")
    return crud.update_item(
        db,
        item,
        name=payload.name,
        quantity=payload.quantity,
        location=payload.location
    )

@app.get("/inventory/low-stock", dependencies=[Depends(require_api_key)])
def low_stock(threshold: int = 10, db: Session = Depends(get_db)):
    return crud.low_stock(db, threshold)

# --- KPIs ---
@app.get("/kpis/today", dependencies=[Depends(require_api_key)])
def kpis_today(db: Session = Depends(get_db)):
    return crud.kpis_today(db)
