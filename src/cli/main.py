# src/cli/main.py
import argparse
import json
from src.services import product_service, order_service, customer_service, report_service

ProductService = product_service.ProductService
CustomerService = customer_service.CustomerService
OrderService = order_service.OrderService
ReportService = report_service.ReportService

class RetailCLI:
    def __init__(self):
        self.prod_service = ProductService()
        self.cust_service = CustomerService()
        self.order_service = OrderService()
        self.report_service = ReportService()

    # ---------------------- Product Commands ---------------------- #
    def cmd_product_add(self, args):
        try:
            p = self.prod_service.add_product(args.name, args.sku, args.price, args.stock, args.category)
            print("✅ Product added:")
            print(json.dumps(p, indent=2, default=str))
        except Exception as e:
            print("❌ Error:", e)

    def cmd_product_list(self, args):
        try:
            ps = self.prod_service.list_products(category=args.category)
            print(json.dumps(ps, indent=2, default=str))
        except Exception as e:
            print("❌ Error:", e)

    # ---------------------- Customer Commands ---------------------- #
    def cmd_customer_add(self, args):
        try:
            c = self.cust_service.create_customer(args.name, args.email, args.phone, args.city)
            print("✅ Customer added:")
            print(json.dumps(c, indent=2, default=str))
        except Exception as e:
            print("❌ Error:", e)

    def cmd_customer_update(self, args):
        try:
            c = self.cust_service.update_customer(args.customer, args.phone, args.city)
            print("✅ Customer updated:")
            print(json.dumps(c, indent=2, default=str))
        except Exception as e:
            print("❌ Error:", e)

    def cmd_customer_delete(self, args):
        try:
            c = self.cust_service.delete_customer(args.customer)
            print("✅ Customer deleted:")
            print(json.dumps(c, indent=2, default=str))
        except Exception as e:
            print("❌ Error:", e)

    def cmd_customer_list(self, args):
        try:
            customers = self.cust_service.list_customers()
            print(json.dumps(customers, indent=2, default=str))
        except Exception as e:
            print("❌ Error:", e)

    def cmd_customer_search(self, args):
        try:
            res = self.cust_service.search_customers(args.email, args.city)
            print(json.dumps(res, indent=2, default=str))
        except Exception as e:
            print("❌ Error:", e)

    # ---------------------- Order Commands ---------------------- #
    def cmd_order_create(self, args):
        items = []
        for item in args.item:
            try:
                pid, qty = item.split(":")
                items.append({"prod_id": int(pid), "quantity": int(qty)})
            except Exception:
                print("❌ Invalid item format:", item)
                return
        try:
            order = self.order_service.create_order(args.customer, items)
            print("✅ Order created:")
            print(json.dumps(order, indent=2, default=str))
        except Exception as e:
            print("❌ Error:", e)

    def cmd_order_show(self, args):
        try:
            o = self.order_service.get_order_details(args.order)
            print(json.dumps(o, indent=2, default=str))
        except Exception as e:
            print("❌ Error:", e)

    def cmd_order_list(self, args):
        try:
            orders = self.order_service.list_orders_by_customer(args.customer)
            print(json.dumps(orders, indent=2, default=str))
        except Exception as e:
            print("❌ Error:", e)

    def cmd_order_cancel(self, args):
        try:
            o = self.order_service.cancel_order(args.order)
            print("✅ Order cancelled:")
            print(json.dumps(o, indent=2, default=str))
        except Exception as e:
            print("❌ Error:", e)

    def cmd_order_complete(self, args):
        try:
            o = self.order_service.complete_order(args.order)
            print("✅ Order completed:")
            print(json.dumps(o, indent=2, default=str))
        except Exception as e:
            print("❌ Error:", e)

    # ---------------------- Reporting Commands ---------------------- #
    def cmd_report_top_products(self, args):
        try:
            res = self.report_service.top_selling_products()
            print(json.dumps(res, indent=2, default=str))
        except Exception as e:
            print("❌ Error:", e)

    def cmd_report_total_revenue(self, args):
        try:
            rev = self.report_service.total_revenue_last_month()
            print(f"💰 Total revenue last month: {rev}")
        except Exception as e:
            print("❌ Error:", e)

    def cmd_report_orders_per_customer(self, args):
        try:
            data = self.report_service.total_orders_per_customer()
            print(json.dumps(data, indent=2, default=str))
        except Exception as e:
            print("❌ Error:", e)

    def cmd_report_frequent_customers(self, args):
        try:
            data = self.report_service.frequent_customers()
            print(json.dumps(data, indent=2, default=str))
        except Exception as e:
            print("❌ Error:", e)

    # ---------------------- CLI Parser ---------------------- #
    def build_parser(self):
        parser = argparse.ArgumentParser(prog="retail-cli")
        sub = parser.add_subparsers(dest="cmd")

        # Product
        p_prod = sub.add_parser("product", help="Product commands")
        pprod_sub = p_prod.add_subparsers(dest="action")
        addp = pprod_sub.add_parser("add")
        addp.add_argument("--name", required=True)
        addp.add_argument("--sku", required=True)
        addp.add_argument("--price", type=float, required=True)
        addp.add_argument("--stock", type=int, default=0)
        addp.add_argument("--category")
        addp.set_defaults(func=self.cmd_product_add)

        listp = pprod_sub.add_parser("list")
        listp.add_argument("--category")
        listp.set_defaults(func=self.cmd_product_list)

        # Customer
        pcust = sub.add_parser("customer", help="Customer commands")
        pcust_sub = pcust.add_subparsers(dest="action")
        addc = pcust_sub.add_parser("add")
        addc.add_argument("--name", required=True)
        addc.add_argument("--email", required=True)
        addc.add_argument("--phone", required=True)
        addc.add_argument("--city")
        addc.set_defaults(func=self.cmd_customer_add)

        updatec = pcust_sub.add_parser("update")
        updatec.add_argument("--customer", type=int, required=True)
        updatec.add_argument("--phone")
        updatec.add_argument("--city")
        updatec.set_defaults(func=self.cmd_customer_update)

        deletec = pcust_sub.add_parser("delete")
        deletec.add_argument("--customer", type=int, required=True)
        deletec.set_defaults(func=self.cmd_customer_delete)

        listc = pcust_sub.add_parser("list")
        listc.set_defaults(func=self.cmd_customer_list)

        searchc = pcust_sub.add_parser("search")
        searchc.add_argument("--email")
        searchc.add_argument("--city")
        searchc.set_defaults(func=self.cmd_customer_search)

        # Order
        porder = sub.add_parser("order", help="Order commands")
        porder_sub = porder.add_subparsers(dest="action")
        createo = porder_sub.add_parser("create")
        createo.add_argument("--customer", type=int, required=True)
        createo.add_argument("--item", required=True, nargs="+", help="prod_id:qty")
        createo.set_defaults(func=self.cmd_order_create)

        showo = porder_sub.add_parser("show")
        showo.add_argument("--order", type=int, required=True)
        showo.set_defaults(func=self.cmd_order_show)

        listo = porder_sub.add_parser("list")
        listo.add_argument("--customer", type=int, required=True)
        listo.set_defaults(func=self.cmd_order_list)

        canco = porder_sub.add_parser("cancel")
        canco.add_argument("--order", type=int, required=True)
        canco.set_defaults(func=self.cmd_order_cancel)

        compo = porder_sub.add_parser("complete")
        compo.add_argument("--order", type=int, required=True)
        compo.set_defaults(func=self.cmd_order_complete)

        # Report
        prep = sub.add_parser("report", help="Reports")
        prep_sub = prep.add_subparsers(dest="action")
        top_prod = prep_sub.add_parser("top_products")
        top_prod.set_defaults(func=self.cmd_report_top_products)
        rev = prep_sub.add_parser("total_revenue")
        rev.set_defaults(func=self.cmd_report_total_revenue)
        orders_pc = prep_sub.add_parser("orders_per_customer")
        orders_pc.set_defaults(func=self.cmd_report_orders_per_customer)
        freq_cust = prep_sub.add_parser("frequent_customers")
        freq_cust.set_defaults(func=self.cmd_report_frequent_customers)

        return parser

    def run(self):
        parser = self.build_parser()
        args = parser.parse_args()
        if not hasattr(args, "func"):
            parser.print_help()
            return
        args.func(args)


if __name__ == "__main__":
    RetailCLI().run()
