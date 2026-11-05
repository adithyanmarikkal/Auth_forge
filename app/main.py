from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import get_db

app=FastAPI()


@app.get("/")
def home():
    return {"message": "Authentication API is running"}


@app.get("/db-test")
def test_database(db: Session = Depends(get_db)):

    result = db.execute(text("SELECT 1"))

    return {
        "message": "Database connected successfully!",
        "result": result.scalar()
    }
