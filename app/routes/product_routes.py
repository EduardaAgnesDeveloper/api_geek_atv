from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from service import ProductService
from models import Produto

router = APIRouter()
service = ProductService()

class ProductCreate(BaseModel):
    nome: str
    descricao: str
    preco: float
    quantidade_estoque: int
    categoria: str
    franquia: str

class ProductUpdate(BaseModel):
    nome: Optional[str]
    descricao: Optional[str]
    preco: Optional[float]
    quantidade_estoque: Optional[int]
    categoria: Optional[str]
    franquia: Optional[str]

@router.post("/products/", response_model=Produto)
def create_product(product: ProductCreate):
    produto = Produto(**product.dict())
    return service.create_product(produto)

@router.get("/products/", response_model=List[Produto])
def read_products(name: Optional[str] = None, price: Optional[float] = None, category: Optional[str] = None, franquia: Optional[str] = None):
    return service.get_products(name, price, category, franquia)

@router.put("/products/{product_id}", response_model=Produto)
def update_product(product_id: int, product: ProductUpdate):
    existing_product = service.update_product(product_id, Produto(**product.dict(exclude_unset=True)))
    if existing_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return existing_product

@router.delete("/products/{product_id}")
def delete_product(product_id: int):
    if not service.delete_product(product_id):
        raise HTTPException(status_code=404, detail="Product not found or not eligible for deletion")
    return {"message": "Product deleted"}

@router.patch("/products/{product_id}/stock", response_model=Produto)
def update_stock(product_id: int, quantity: int):
    updated_product = service.update_stock(product_id, quantity)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product not found or insufficient stock")
    return updated_product
