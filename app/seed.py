from app.db import SessionLocal, engine, Base
from app import crud, models

def get_or_create_item(db, sku: str, name: str, quantity: int, location: str):
    existing = db.query(models.InventoryItem).filter(models.InventoryItem.sku == sku).first()
    if existing:
        # update fields to keep demo consistent
        existing.name = name
        existing.quantity = quantity
        existing.location = location
        db.commit()
        db.refresh(existing)
        return existing
    return crud.create_item(db, sku=sku, name=name, quantity=quantity, location=location)

def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Create a demo worker (always new)
        w = crud.create_worker(db, name="Demo Worker", role="OFA", shift="day")

        # Inventory (idempotent)
        get_or_create_item(db, sku="HD-1001", name="Cordless Drill", quantity=6, location="Aisle 12")
        get_or_create_item(db, sku="HD-2002", name="Work Gloves", quantity=2, location="Aisle 3")

        # Orders (new each run)
        o1 = crud.create_order(db, channel="pickup", promised_minutes=60, worker_id=w.id)
        o2 = crud.create_order(db, channel="delivery", promised_minutes=45, worker_id=w.id)

        # Mark complete: one on-time, one late
        crud.update_order(db, o1, status="ready", pick_time_minutes=38)  # on-time
        crud.update_order(db, o2, status="ready", pick_time_minutes=50)  # late

        print("Seed complete ✅")
        print(f"Worker id: {w.id}")
        print(f"Order ids: {o1.id}, {o2.id}")
    finally:
        db.close()

if __name__ == "__main__":
    run()
