from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel
import psycopg2
from typing import List
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'telemetry')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

if not all([DB_USER, DB_PASSWORD]):
    raise ValueError('Database credentials are not set')

def get_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    try:
        yield conn
    finally:
        conn.close()

class Telemetry(BaseModel):
    id: int
    timestamp: int
    value: float
    status: int

@app.get("/api/v1/telemetry", response_model=List[Telemetry])
def get_telemetry(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db=Depends(get_db)
):
    offset = (page - 1) * page_size
    cursor = db.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT id, timestamp, value, status FROM telemetry ORDER BY timestamp DESC LIMIT %s OFFSET %s", (page_size, offset))
        records = cursor.fetchall()
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

