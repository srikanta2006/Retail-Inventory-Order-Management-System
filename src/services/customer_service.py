from typing import Dict, List
from src.dao.customer_dao import customerDAO

class CustomerError(Exception): pass

class CustomerService:
    def __init__(self):
        self.dao = customerDAO()

    def create_customer(self, name: str, email: str, phone: str, city: str | None = None) -> Dict:
        return self.dao.create_customer(name, email, phone, city)

    def update_customer(self, cust_id: int, phone: str | None = None, city: str | None = None) -> Dict:
        fields = {}
        if phone: fields["phone"] = phone
        if city: fields["city"] = city
        if not fields: raise ValueError("Provide phone or city to update")
        return self.dao.update_customer(cust_id, fields)

    def delete_customer(self, cust_id: int) -> Dict:
        return self.dao.delete_customer(cust_id)

    def list_customers(self) -> List[Dict]:
        return self.dao.list_customers()

    def search_customers(self, email: str | None = None, city: str | None = None) -> List[Dict]:
        return self.dao.search_customers(email, city)
