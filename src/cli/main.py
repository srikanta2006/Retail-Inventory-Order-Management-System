# src/cli/main.py
import argparse
import json

from src.services.product_service import ProductService
# from src.services.customer_service import CustomerService
# from src.services.order_service import OrderService


class RetailCLI:
    def __init__(self):
        # Initialize service objects
        self.product_service = ProductService()
        # self.customer_service = CustomerService()
        # self.order_service = OrderService()

    # ---------------------- Product Commands ---------------------- #
    def cmd_product_add(self, args):
        try:
            p = self.product_service.add_product(
                args.name, args.sku, args.price, args.stock, args.category
            )
            print("✅ Created product:")
            print(json.dumps(p, indent=2, default=str))
        except Exception as e:
            print("❌ Error:", e)

    def cmd_product_list(self, args):
        ps = self.product_service.list_products(limit=100)
        print(json.dumps(ps, indent=2, default=str))

    # ---------------------- Customer Commands ---------------------- #
    def cmd_customer_add(self, args):
        # Placeholder – hook CustomerService here
        try:
            print("⚠ Customer service not implemented yet.")
            # c = self.customer_service.create_customer(args.name, args.email, args.phone, args.city)
            # print("✅ Created customer:")
            # print(json.dumps(c, indent=2, default=str))
        except Exception as e:
            print("❌ Error:", e)

    # ---------------------- Order Commands ---------------------- #
    def cmd_order_create(self, args):
        # items provided as prod_id:qty strings
        items = []
        for item in args.item:
            try:
                pid, qty = item.split(":")
                items.append({"prod_id": int(pid), "quantity": int(qty)})
            except Exception:
                print("❌ Invalid item format:", item)
                return
        try:
            print("⚠ Order service not implemented yet.")
            # ord = self.order_service.create_order(args.customer, items)
            # print("✅ Order created:")
            # print(json.dumps(ord, indent=2, default=str))
        except Exception as e:
            print("❌ Error:", e)

    def cmd_order_show(self, args):
        try:
            print("⚠ Order service not implemented yet.")
            # o = self.order_service.get_order_details(args.order)
            # print(json.dumps(o, indent=2, default=str))
        except Exception as e:
            print("❌ Error:", e)

    def cmd_order_cancel(self, args):
        try:
            print("⚠ Order service not implemented yet.")
            # o = self.order_service.cancel_order(args.order)
            # print("✅ Order cancelled (updated):")
            # print(json.dumps(o, indent=2, default=str))
        except Exception as e:
            print("❌ Error:", e)

    # ---------------------- Parser Builder ---------------------- #
    def build_parser(self):
        parser = argparse.ArgumentParser(prog="retail-cli")
        sub = parser.add_subparsers(dest="cmd")

        # product add/list
        p_prod = sub.add_parser("product", help="product commands")
        pprod_sub = p_prod.add_subparsers(dest="action")

        addp = pprod_sub.add_parser("add")
        addp.add_argument("--name", required=True)
        addp.add_argument("--sku", required=True)
        addp.add_argument("--price", type=float, required=True)
        addp.add_argument("--stock", type=int, default=0)
        addp.add_argument("--category", default=None)
        addp.set_defaults(func=self.cmd_product_add)

        listp = pprod_sub.add_parser("list")
        listp.set_defaults(func=self.cmd_product_list)

        # customer add
        pcust = sub.add_parser("customer", help="customer commands")
        pcust_sub = pcust.add_subparsers(dest="action")

        addc = pcust_sub.add_parser("add")
        addc.add_argument("--name", required=True)
        addc.add_argument("--email", required=True)
        addc.add_argument("--phone", required=True)
        addc.add_argument("--city", default=None)
        addc.set_defaults(func=self.cmd_customer_add)

        # order create/show/cancel
        porder = sub.add_parser("order", help="order commands")
        porder_sub = porder.add_subparsers(dest="action")

        createo = porder_sub.add_parser("create")
        createo.add_argument("--customer", type=int, required=True)
        createo.add_argument("--item", required=True, nargs="+", help="prod_id:qty (repeatable)")
        createo.set_defaults(func=self.cmd_order_create)

        showo = porder_sub.add_parser("show")
        showo.add_argument("--order", type=int, required=True)
        showo.set_defaults(func=self.cmd_order_show)

        cano = porder_sub.add_parser("cancel")
        cano.add_argument("--order", type=int, required=True)
        cano.set_defaults(func=self.cmd_order_cancel)

        return parser

    # ---------------------- Main Entrypoint ---------------------- #
    def run(self):
        parser = self.build_parser()
        args = parser.parse_args()
        if not hasattr(args, "func"):
            parser.print_help()
            return
        args.func(args)


if __name__ == "__main__":
    RetailCLI().run()
