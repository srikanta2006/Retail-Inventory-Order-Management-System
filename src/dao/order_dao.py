from typing import List, Dict
from src.config import get_supabase
from src.dao.product_dao import ProductDAO
from src.dao.customer_dao import customerDAO

class orderDAO:
    def __init__(self):
        self._sb = get_supabase()
        self.prod_dao = ProductDAO()
        self.cust_dao = customerDAO()

    def create_order(self, cust_id: int, items: List[Dict], total_amount: float) -> Dict:
        order_payload = {"cust_id": cust_id, "total_amount": total_amount, "status": "PLACED"}
        resp_order = self._sb.table("orders").insert(order_payload).execute()
        order_id = resp_order.data[0]["order_id"]

        for item in items:
            self._sb.table("order_items").insert({
                "order_id": order_id,
                "prod_id": item["prod_id"],
                "quantity": item["quantity"],
                "price": item["price"]
            }).execute()

        # create pending payment
        self._sb.table("payments").insert({"order_id": order_id, "amount": total_amount, "status": "PENDING"}).execute()

        return {"order_id": order_id, "cust_id": cust_id, "items": items, "total_amount": total_amount, "status": "PLACED"}

    def get_order_details(self, order_id: int) -> Dict:
        resp_order = self._sb.table("orders").select("*").eq("order_id", order_id).limit(1).execute()
        order = resp_order.data[0] if resp_order.data else None
        if not order: raise ValueError("Order not found")

        customer = self.cust_dao.get_customer_by_id(order["cust_id"])
        resp_items = self._sb.table("order_items").select("*").eq("order_id", order_id).execute()
        items = resp_items.data or []
        for item in items:
            prod = self.prod_dao.get_product_by_id(item["prod_id"])
            if prod:
                item["product_name"] = prod["name"]
                item["product_price"] = prod["price"]

        order["customer"] = customer
        order["items"] = items
        return order

    def list_orders_by_customer(self, cust_id: int) -> List[Dict]:
        resp_orders = self._sb.table("orders").select("*").eq("cust_id", cust_id).execute()
        orders = resp_orders.data or []
        for order in orders:
            resp_items = self._sb.table("order_items").select("*").eq("order_id", order["order_id"]).execute()
            items = resp_items.data or []
            for item in items:
                prod = self.prod_dao.get_product_by_id(item["prod_id"])
                if prod:
                    item["product_name"] = prod["name"]
                    item["product_price"] = prod["price"]
            order["items"] = items
        return orders

    def update_order_status(self, order_id: int, status: str):
        self._sb.table("orders").update({"status": status}).eq("order_id", order_id).execute()
        return self.get_order_details(order_id)
