import requests
from urllib.parse import quote_plus

OPENFOODFACTS_BARCODE_URL = "https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
OPENFOODFACTS_SEARCH_URL = "https://world.openfoodfacts.org/cgi/search.pl"


def fetch_product_info(barcode=None, name=None):
    if barcode:
        return _fetch_by_barcode(barcode)
    if name:
        return _fetch_by_name(name)
    raise ValueError("Provide barcode or name to fetch product information")


def _fetch_by_barcode(barcode):
    url = OPENFOODFACTS_BARCODE_URL.format(barcode=quote_plus(str(barcode)))
    response = requests.get(url, timeout=8)
    if response.status_code != 200:
        raise ValueError("Unable to reach external API")

    data = response.json()
    if data.get("status") != 1 or "product" not in data:
        raise ValueError("Product not found for barcode")

    return _normalize_product(data["product"])


def _fetch_by_name(name):
    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 1,
    }
    response = requests.get(OPENFOODFACTS_SEARCH_URL, params=params, timeout=8)
    if response.status_code != 200:
        raise ValueError("Unable to reach external API")

    data = response.json()
    products = data.get("products") or []
    if not products:
        raise ValueError("Product not found for name")

    return _normalize_product(products[0])


def _normalize_product(product_data):
    return {
        "name": product_data.get("product_name") or product_data.get("generic_name") or "Unknown Product",
        "barcode": product_data.get("code"),
        "description": product_data.get("generic_name") or product_data.get("categories_tags", [""])[0] or "",
        "category": product_data.get("categories_tags", ["uncategorized"])[0].replace("en:", "") if product_data.get("categories_tags") else "uncategorized",
        "brand": product_data.get("brands", ""),
        "ingredients_text": product_data.get("ingredients_text", ""),
    }
