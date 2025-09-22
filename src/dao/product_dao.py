from typing import List, Dict, Optional
from src.config import get_supabase

class ProductDAO:
    def __init__(self):
        self._sb = get_supabase()

    def create_product(self, name: str, sku: str, price: float, stock: int = 0, category: str | None = None) -> Optional[Dict]:
        payload = {"name": name, "sku": sku, "price": price, "stock": stock}
        if category:
            payload["category"] = category
        self._sb.table("products").insert(payload).execute()
        resp = self._sb.table("products").select("*").eq("sku", sku).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_product_by_id(self, prod_id: int) -> Optional[Dict]:
        resp = self._sb.table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def list_products(self, limit: int = 100, category: str | None = None) -> List[Dict]:
        q = self._sb.table("products").select("*").limit(limit)
        if category:
            q = q.eq("category", category)
        resp = q.execute()
        return resp.data or []

    def update_product(self, prod_id: int, fields: Dict) -> Optional[Dict]:
        self._sb.table("products").update(fields).eq("prod_id", prod_id).execute()
        return self.get_product_by_id(prod_id)
