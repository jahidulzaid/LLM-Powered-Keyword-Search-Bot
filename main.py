from fastapi import FastAPI
from app.routes import search

app = FastAPI(title="AI Search Bot", version="1.0.0")

app.include_router(search.router, prefix="/api", tags=["search"])

@app.get("/")
def root():
    return {"message": "AI Search Bot API"}
