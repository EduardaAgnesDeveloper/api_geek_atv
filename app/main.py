from fastapi import FastAPI
from routes.product_routes import router as product_router
from database import create_db_and_tables

app = FastAPI()

create_db_and_tables()

app.include_router(product_router, prefix="/api", tags=["Produtos"])

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Gerenciamento de Produtos"}
