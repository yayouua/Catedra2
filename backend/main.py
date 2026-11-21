import os
from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://appuser:rescue123@db:5432/appdb",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
app = FastAPI(title="ACI606 Docker Rescue API", version="1.0")


class ItemIn(BaseModel):
    name: str = Field(min_length=1, max_length=80)


@app.on_event("startup")
def startup() -> None:
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS items (
                id SERIAL PRIMARY KEY,
                name VARCHAR(80) NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """))


@app.get("/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "reachable"}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"database unavailable: {exc}")


@app.get("/items")
def list_items():
    with engine.connect() as conn:
        rows = conn.execute(
            text("SELECT id, name, created_at FROM items ORDER BY id")
        ).mappings().all()
    return [dict(row) for row in rows]


@app.post("/items", status_code=201)
def create_item(item: ItemIn):
    with engine.begin() as conn:
        row = conn.execute(
            text("INSERT INTO items(name) VALUES (:name) RETURNING id, name, created_at"),
            {"name": item.name},
        ).mappings().one()
    return dict(row)


@app.get("/")
def root():
    return {
        "service": "ACI606 Docker Rescue API",
        "time": datetime.utcnow().isoformat() + "Z",
    }
