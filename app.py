from flask import Flask, jsonify, request, abort
from external_api import fetch_product_info

app = Flask(__name__)

inventory = []
next_id = 1


def reset_inventory():
    """Reset inventory in memory for testing."""
    global inventory, next_id
    inventory.clear()
    next_id = 1


def _find_item(item_id):
    return next((item for item in inventory if item["id"] == item_id), None)


def _find_item_index(item_id):
    for index, item in enumerate(inventory):
        if item["id"] == item_id:
            return index
    return None


@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory), 200


@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    item = _find_item(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200


@app.route("/inventory", methods=["POST"])
def add_inventory_item():
    global next_id
    data = request.get_json(force=True)
    if not data or "name" not in data:
        return jsonify({"error": "Missing required field: name"}), 400

    item = {
        "id": next_id,
        "name": data["name"],
        "barcode": data.get("barcode"),
        "quantity": int(data.get("quantity", 0)),
        "price": float(data.get("price", 0.0)),
        "description": data.get("description", ""),
        "category": data.get("category", "uncategorized"),
    }
    inventory.append(item)
    next_id += 1
    return jsonify(item), 201


@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_inventory_item(item_id):
    item = _find_item(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json(force=True)
    if not data:
        return jsonify({"error": "Missing update payload"}), 400

    for field in ["name", "barcode", "quantity", "price", "description", "category"]:
        if field in data:
            if field == "quantity":
                item[field] = int(data[field])
            elif field == "price":
                item[field] = float(data[field])
            else:
                item[field] = data[field]

    return jsonify(item), 200


@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    index = _find_item_index(item_id)
    if index is None:
        return jsonify({"error": "Item not found"}), 404
    removed = inventory.pop(index)
    return jsonify({"message": "Item deleted", "item": removed}), 200


@app.route("/inventory/search", methods=["GET"])
def search_inventory():
    barcode = request.args.get("barcode")
    name = request.args.get("name")
    if barcode:
        result = [item for item in inventory if item.get("barcode") == barcode]
    elif name:
        result = [item for item in inventory if name.lower() in item.get("name", "").lower()]
    else:
        return jsonify({"error": "Provide barcode or name query parameter"}), 400
    return jsonify(result), 200


@app.route("/inventory/external", methods=["GET"])
def get_external_product():
    barcode = request.args.get("barcode")
    name = request.args.get("name")
    if not barcode and not name:
        return jsonify({"error": "Provide barcode or name query parameter"}), 400

    try:
        product = fetch_product_info(barcode=barcode, name=name)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404
    return jsonify(product), 200


@app.route("/inventory/external", methods=["POST"])
def add_external_product():
    global next_id
    data = request.get_json(force=True)
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    barcode = data.get("barcode")
    name = data.get("name")
    if not barcode and not name:
        return jsonify({"error": "Provide barcode or name in JSON body"}), 400

    try:
        product = fetch_product_info(barcode=barcode, name=name)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404

    item = {
        "id": next_id,
        "name": product.get("name", "Unknown Product"),
        "barcode": product.get("barcode"),
        "quantity": int(data.get("quantity", 1)),
        "price": float(data.get("price", 0.0)),
        "description": product.get("description", ""),
        "category": product.get("category", "uncategorized"),
    }
    inventory.append(item)
    next_id += 1
    return jsonify(item), 201


if __name__ == "__main__":
    app.run(debug=True)
