from typing import List, Dict
from src.dao.product_dao import ProductDAO

class ProductError(Exception): pass

class ProductService:
    def __init__(self):
        self.dao = ProductDAO()

    def add_product(self, name: str, sku: str, price: float, stock: int = 0, category: str | None = None) -> Dict:
        if price <= 0: raise ProductError("Price must be positive")
        return self.dao.create_product(name, sku, price, stock, category)

    def list_products(self, category: str | None = None) -> List[Dict]:
        return self.dao.list_products(category=category)

    def update_stock(self, prod_id: int, delta: int) -> Dict:
        prod = self.dao.get_product_by_id(prod_id)
        if not prod: raise ProductError("Product not found")
        return self.dao.update_product(prod_id, {"stock": prod["stock"] + delta})
