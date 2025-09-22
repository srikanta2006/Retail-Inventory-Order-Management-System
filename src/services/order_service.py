from typing import List, Dict
from src.dao.order_dao import orderDAO
from src.dao.customer_dao import customerDAO
from src.dao.product_dao import ProductDAO

class OrderError(Exception): pass

class OrderService:
    def __init__(self):
        self.dao = orderDAO()
        self.cust_dao = customerDAO()
        self.prod_dao = ProductDAO()

    def create_order(self, cust_id: int, items: List[Dict]) -> Dict:
        customer = self.cust_dao.get_customer_by_id(cust_id)
        if not customer: raise OrderError("Customer not found")

        total_amount = 0
        prepared_items = []

        for item in items:
            prod = self.prod_dao.get_product_by_id(item["prod_id"])
            if not prod: raise OrderError(f"Product not found: {item['prod_id']}")
            if prod["stock"] < item["quantity"]:
                raise OrderError(f"Not enough stock for {prod['name']}")
            self.prod_dao.update_product(prod["prod_id"], {"stock": prod["stock"] - item["quantity"]})
            prepared_items.append({"prod_id": prod["prod_id"], "quantity": item["quantity"], "price": prod["price"]})
            total_amount += prod["price"] * item["quantity"]

        return self.dao.create_order(cust_id, prepared_items, total_amount)

    def get_order_details(self, order_id: int) -> Dict:
        return self.dao.get_order_details(order_id)

    def list_orders_by_customer(self, cust_id: int) -> List[Dict]:
        return self.dao.list_orders_by_customer(cust_id)

    def cancel_order(self, order_id: int) -> Dict:
        order = self.dao.get_order_details(order_id)
        if order["status"] != "PLACED": raise OrderError("Only PLACED orders can be cancelled")
        for item in order["items"]:
            prod = self.prod_dao.get_product_by_id(item["prod_id"])
            self.prod_dao.update_product(prod["prod_id"], {"stock": prod["stock"] + item["quantity"]})
        self.dao.update_order_status(order_id, "CANCELLED")
        # update payment to REFUNDED
        self.dao._sb.table("payments").update({"status": "REFUNDED"}).eq("order_id", order_id).execute()
        return self.dao.get_order_details(order_id)

    def complete_order(self, order_id: int) -> Dict:
        order = self.dao.get_order_details(order_id)
        if order["status"] != "PLACED": raise OrderError("Only PLACED orders can be completed")
        self.dao.update_order_status(order_id, "COMPLETED")
        # mark payment as PAID
        self.dao._sb.table("payments").update({"status": "PAID"}).eq("order_id", order_id).execute()
        return self.dao.get_order_details(order_id)
