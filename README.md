# Retail Operations REST API (FastAPI)

Backend API that models retail fulfillment operations: workers, orders, inventory, and operational KPIs.

## Features
- API key auth via `x-api-key`
- CRUD endpoints for workers, orders, and inventory
- Operational analytics:
  - `/kpis/today` (on-time rate, avg pick time, completions)
  - `/inventory/low-stock` (threshold-based alerts)
  - `/workers/{id}/performance` (worker-level KPIs)
- Auto-generated OpenAPI docs at `/docs`
- Seed script for instant demo data

## Tech Stack
- Python, FastAPI
- SQLAlchemy ORM
- SQLite (local dev)

## Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001

