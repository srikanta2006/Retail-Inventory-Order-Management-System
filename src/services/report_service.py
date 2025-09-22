# src/services/report_service.py
from src.dao.order_dao import orderDAO
from src.dao.product_dao import ProductDAO
from src.dao.customer_dao import customerDAO
from datetime import datetime, timedelta

class ReportService:
    def __init__(self):
        self.order_dao = orderDAO()
        self.prod_dao = ProductDAO()
        self.cust_dao = customerDAO()

    def top_selling_products(self, top_n=5):
        orders = self.order_dao.get_all_orders()  # implement in DAO if needed
        product_sales = {}
        for order in orders:
            for item in order.get("items", []):
                pid = item["prod_id"]
                product_sales[pid] = product_sales.get(pid, 0) + item["quantity"]

        sorted_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)
        top_products = []
        for pid, qty in sorted_products[:top_n]:
            prod = self.prod_dao.get_product_by_id(pid)
            if prod:
                top_products.append({"prod_id": pid, "name": prod["name"], "sold_quantity": qty})
        return top_products

    def total_revenue_last_month(self):
        today = datetime.today()
        first_day_last_month = datetime(today.year, today.month - 1, 1)
        last_day_last_month = datetime(today.year, today.month, 1) - timedelta(days=1)

        orders = self.order_dao.get_all_orders()
        total = 0
        for order in orders:
            created = datetime.fromisoformat(order.get("created_at", today.isoformat()))
            if first_day_last_month <= created <= last_day_last_month:
                total += order.get("total_amount", 0)
        return total

    def total_orders_per_customer(self):
        orders = self.order_dao.get_all_orders()
        counts = {}
        for order in orders:
            cid = order["cust_id"]
            counts[cid] = counts.get(cid, 0) + 1
        result = []
        for cid, count in counts.items():
            cust = self.cust_dao.get_customer_by_id(cid)
            if cust:
                result.append({"customer": cust, "orders_count": count})
        return result

    def frequent_customers(self, min_orders=3):
        all_orders = self.total_orders_per_customer()
        return [c for c in all_orders if c["orders_count"] >= min_orders]
