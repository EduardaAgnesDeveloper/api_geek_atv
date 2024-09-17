from typing import List, Optional
from models import Produto
from database import get_session

class ProductService:
    def __init__(self):
        self.db_session = get_session()

    def create_product(self, produto: Produto) -> Produto:
        with self.db_session() as session:
            session.add(produto)
            session.commit()
            session.refresh(produto)
            return produto

    def get_products(self, name: Optional[str] = None, price: Optional[float] = None, category: Optional[str] = None, franquia: Optional[str] = None) -> List[Produto]:
        with self.db_session() as session:
            query = select(Produto)
            if name:
                query = query.where(Produto.nome == name)
            if price:
                query = query.where(Produto.preco == price)
            if category:
                query = query.where(Produto.categoria == category)
            if franquia:
                query = query.where(Produto.franquia == franquia)
            result = session.exec(query)
            return result.all()

    def update_product(self, product_id: int, updated_product: Produto) -> Optional[Produto]:
        with self.db_session() as session:
            product = session.get(Produto, product_id)
            if product:
                product.nome = updated_product.nome
                product.descricao = updated_product.descricao
                product.preco = updated_product.preco
                product.quantidade_estoque = updated_product.quantidade_estoque
                product.categoria = updated_product.categoria
                product.franquia = updated_product.franquia
                session.commit()
                session.refresh(product)
                return product
            return None

    def delete_product(self, product_id: int) -> bool:
        with self.db_session() as session:
            product = session.get(Produto, product_id)
            if product and product.quantidade_estoque == 0:
                session.delete(product)
                session.commit()
                return True
            return False

    def update_stock(self, product_id: int, quantity: int) -> Optional[Produto]:
        with self.db_session() as session:
            product = session.get(Produto, product_id)
            if product:
                if quantity < 0 and product.quantidade_estoque + quantity < 0:
                    return None  
                product.quantidade_estoque += quantity
                session.commit()
                session.refresh(product)
                return product
            return None
