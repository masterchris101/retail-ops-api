# Retail Operations REST API (FastAPI)

Backend REST API that models retail fulfillment operations, including workers, orders, inventory, and operational KPI analytics.

## Features
- API key authentication via `x-api-key`
- CRUD endpoints for workers, orders, and inventory
- Operational analytics endpoints:
  - `/kpis/today` — on-time rate, average pick time, completed orders
  - `/inventory/low-stock` — threshold-based inventory alerts
  - `/workers/{id}/performance` — worker-level performance metrics
- Auto-generated OpenAPI documentation at `/docs`
- Seed script for instant demo data

## Tech Stack
- Python
- FastAPI
- SQLAlchemy ORM
- SQLite (local development)

---

## Demo (1 minute)

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set API key
echo "API_KEY=dev-key" > .env

# Start the API
uvicorn app.main:app --reload --port 8001
Open API docs:

arduino
Copy code
http://127.0.0.1:8001/docs
Seed demo data
bash
Copy code
PYTHONPATH=. python3 app/seed.py
Example requests
bash
Copy code
# Get KPIs
curl -X GET "http://127.0.0.1:8001/kpis/today" \
  -H "x-api-key: dev-key"

# Low stock alerts
curl -X GET "http://127.0.0.1:8001/inventory/low-stock?threshold=3" \
  -H "x-api-key: dev-key"

# Worker performance (example)
curl -X GET "http://127.0.0.1:8001/workers/8/performance" \
  -H "x-api-key: dev-key"
API Endpoints
Workers
POST /workers

GET /workers

GET /workers/{id}

GET /workers/{id}/performance

Orders
POST /orders

GET /orders

PATCH /orders/{id}

Inventory
POST /inventory

GET /inventory

PATCH /inventory/{id}

GET /inventory/low-stock

KPIs
GET /kpis/today

Design Notes
Relational data model using SQLAlchemy

API-key authentication enforced via dependency injection

KPI endpoints compute analytics from real operational data

Seed script is idempotent for repeatable demos

Future Improvements
Pagination and filtering

JWT-based authentication

Frontend dashboard (React)

Dockerized deployment

Author
Cristian Novelle-Ruddy
GitHub: https://github.com/masterchris101

yaml
Copy code

---

### After pasting
Run these commands:

```bash
git add README.md
git commit -m "Polish README with demo and API documentation"
git push
