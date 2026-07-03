"""Tests as short scenes: each function tells a tiny story about the API.

Read each test like a step in a user's journey: add an item, fetch the list,
update quantities, and consult the external product source.
"""

import json
import pytest
from app import app, inventory, reset_inventory


@pytest.fixture(autouse=True)
def client():
    """Scene setter: ensure each test begins with a clean inventory."""
    reset_inventory()
    with app.test_client() as client:
        yield client


def test_add_item(client):
    """Scene: a user adds an Apple to the empty shelf and checks it was stored."""
    response = client.post("/inventory", json={"name": "Apple", "quantity": 10, "price": 1.5})
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Apple"
    assert data["quantity"] == 10
    assert data["price"] == 1.5


def test_get_inventory(client):
    """Scene: after adding an item, the inventory list shows exactly one entry."""
    client.post("/inventory", json={"name": "Apple"})
    response = client.get("/inventory")
    assert response.status_code == 200
    assert len(response.get_json()) == 1


def test_get_item_by_id(client):
    """Scene: a Banana is placed on shelf #1; we fetch shelf #1 and read the label."""
    client.post("/inventory", json={"name": "Banana"})
    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["name"] == "Banana"


def test_update_item(client):
    """Scene: inventory grows—we update Banana's quantity and price."""
    client.post("/inventory", json={"name": "Banana", "quantity": 5})
    response = client.patch("/inventory/1", json={"quantity": 10, "price": 2.0})
    assert response.status_code == 200
    data = response.get_json()
    assert data["quantity"] == 10
    assert data["price"] == 2.0


def test_delete_item(client):
    """Scene: the Banana is removed; the shelf is empty again."""
    client.post("/inventory", json={"name": "Banana"})
    response = client.delete("/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Item deleted"


def test_search_inventory(client):
    """Scene: two items are present; we search by name and find the Apple."""
    client.post("/inventory", json={"name": "Banana", "barcode": "123"})
    client.post("/inventory", json={"name": "Apple", "barcode": "456"})
    response = client.get("/inventory/search", query_string={"name": "apple"})
    assert response.status_code == 200
    assert len(response.get_json()) == 1


def test_search_not_found(client):
    """Scene: a search without criteria should politely ask for input."""
    response = client.get("/inventory/search")
    assert response.status_code == 400


def test_external_fetch_invalid(client, monkeypatch):
    """Scene: external lookup fails and the API returns a not-found response."""
    from external_api import fetch_product_info

    def fail_fetch(*args, **kwargs):
        raise ValueError("Product not found")

    monkeypatch.setattr("external_api.fetch_product_info", fail_fetch)
    response = client.get("/inventory/external", query_string={"barcode": "000"})
    assert response.status_code == 404


def test_add_external_product_invalid(client, monkeypatch):
    """Scene: attempting to add an unavailable external product returns not-found."""
    def fail_fetch(*args, **kwargs):
        raise ValueError("Product not found")

    monkeypatch.setattr("external_api.fetch_product_info", fail_fetch)
    response = client.post("/inventory/external", json={"barcode": "000"})
    assert response.status_code == 404
