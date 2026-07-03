import argparse
import requests

API_BASE = "http://127.0.0.1:5000"


def list_items(args):
    response = requests.get(f"{API_BASE}/inventory")
    print(response.json())


def get_item(args):
    response = requests.get(f"{API_BASE}/inventory/{args.id}")
    print(response.json())


def add_item(args):
    payload = {
        "name": args.name,
        "barcode": args.barcode,
        "quantity": args.quantity,
        "price": args.price,
        "description": args.description,
        "category": args.category,
    }
    response = requests.post(f"{API_BASE}/inventory", json=payload)
    print(response.json())


def update_item(args):
    payload = {}
    for field in ["name", "barcode", "quantity", "price", "description", "category"]:
        value = getattr(args, field, None)
        if value is not None:
            payload[field] = value
    response = requests.patch(f"{API_BASE}/inventory/{args.id}", json=payload)
    print(response.json())


def delete_item(args):
    response = requests.delete(f"{API_BASE}/inventory/{args.id}")
    print(response.json())


def search_items(args):
    params = {}
    if args.barcode:
        params["barcode"] = args.barcode
    if args.name:
        params["name"] = args.name
    response = requests.get(f"{API_BASE}/inventory/search", params=params)
    print(response.json())


def external_fetch(args):
    params = {}
    if args.barcode:
        params["barcode"] = args.barcode
    if args.name:
        params["name"] = args.name
    response = requests.get(f"{API_BASE}/inventory/external", params=params)
    print(response.json())


def external_add(args):
    payload = {}
    if args.barcode:
        payload["barcode"] = args.barcode
    if args.name:
        payload["name"] = args.name
    if args.quantity is not None:
        payload["quantity"] = args.quantity
    if args.price is not None:
        payload["price"] = args.price
    response = requests.post(f"{API_BASE}/inventory/external", json=payload)
    print(response.json())


def main():
    parser = argparse.ArgumentParser(description="Inventory management CLI for Flask API")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List all inventory items").set_defaults(func=list_items)

    get_parser = subparsers.add_parser("get", help="Get a single item by ID")
    get_parser.add_argument("id", type=int)
    get_parser.set_defaults(func=get_item)

    add_parser = subparsers.add_parser("add", help="Add a new inventory item")
    add_parser.add_argument("name")
    add_parser.add_argument("--barcode")
    add_parser.add_argument("--quantity", type=int, default=0)
    add_parser.add_argument("--price", type=float, default=0.0)
    add_parser.add_argument("--description", default="")
    add_parser.add_argument("--category", default="uncategorized")
    add_parser.set_defaults(func=add_item)

    update_parser = subparsers.add_parser("update", help="Update inventory item fields")
    update_parser.add_argument("id", type=int)
    update_parser.add_argument("--name")
    update_parser.add_argument("--barcode")
    update_parser.add_argument("--quantity", type=int)
    update_parser.add_argument("--price", type=float)
    update_parser.add_argument("--description")
    update_parser.add_argument("--category")
    update_parser.set_defaults(func=update_item)

    delete_parser = subparsers.add_parser("delete", help="Delete an item by ID")
    delete_parser.add_argument("id", type=int)
    delete_parser.set_defaults(func=delete_item)

    search_parser = subparsers.add_parser("search", help="Search inventory by name or barcode")
    search_parser.add_argument("--barcode")
    search_parser.add_argument("--name")
    search_parser.set_defaults(func=search_items)

    fetch_parser = subparsers.add_parser("fetch", help="Fetch product details from external API")
    fetch_parser.add_argument("--barcode")
    fetch_parser.add_argument("--name")
    fetch_parser.set_defaults(func=external_fetch)

    add_external_parser = subparsers.add_parser("add-external", help="Fetch from external API and add to inventory")
    add_external_parser.add_argument("--barcode")
    add_external_parser.add_argument("--name")
    add_external_parser.add_argument("--quantity", type=int)
    add_external_parser.add_argument("--price", type=float)
    add_external_parser.set_defaults(func=external_add)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
