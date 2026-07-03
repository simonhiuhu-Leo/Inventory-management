"""Narrative tests for successful external API interactions.

These tests mock `external_api.fetch_product_info` to simulate a friendly
third-party response and assert that the app consumes the data correctly.
"""

import pytest
from app import app, reset_inventory


@pytest.fixture()
def client():
    reset_inventory()
    with app.test_client() as client:
        yield client


def test_get_external_product_success(client, monkeypatch):
    """Scene: the external API returns product info for a barcode."""

    def mock_fetch(barcode=None, name=None):
        return {
            "name": "Mock Cereal",
            "barcode": barcode or "000",
            "description": "A crunchy mock cereal",
            "category": "breakfast",
            "brand": "MockBrand",
            "ingredients_text": "grain, sugar",
        }

    monkeypatch.setattr("app.fetch_product_info", mock_fetch)
    response = client.get("/inventory/external", query_string={"barcode": "000"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Mock Cereal"


def test_add_external_product_success(client, monkeypatch):
    """Scene: user asks to add an externally-fetched product into inventory."""

    def mock_fetch(barcode=None, name=None):
        return {
            "name": "Mock Cereal",
            "barcode": barcode or "000",
            "description": "A crunchy mock cereal",
            "category": "breakfast",
            "brand": "MockBrand",
            "ingredients_text": "grain, sugar",
        }

    monkeypatch.setattr("app.fetch_product_info", mock_fetch)
    response = client.post("/inventory/external", json={"barcode": "000", "quantity": 3, "price": 4.5})
    assert response.status_code == 201
    item = response.get_json()
    assert item["name"] == "Mock Cereal"
    assert item["barcode"] == "000"
    assert item["quantity"] == 3
    assert item["price"] == 4.5
