# Inventory Management System

This repository contains a Python Flask REST API for managing inventory items.
The service supports CRUD operations, external product enrichment via OpenFoodFacts,
and a CLI for command-line interaction.

## Features

- CRUD inventory endpoints (`GET`, `POST`, `PATCH`, `DELETE`).
- Search inventory by `name` or `barcode`.
- Fetch product details from OpenFoodFacts by barcode or name.
- Add external products directly into inventory.
- CLI interface for admin-style workflow operations.
- Automated tests with `pytest`.

## Setup

Run these commands from the repository root.

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the API

Start the Flask application:

```bash
python app.py
```

The API is available at `http://127.0.0.1:5000`.

## CLI Usage

Use the CLI to interact with the API from the command line:

```bash
python cli.py list
python cli.py add "Garden Apple" --barcode 12345 --quantity 10 --price 1.99
python cli.py get 1
python cli.py update 1 --quantity 12
python cli.py delete 1
python cli.py fetch --barcode 737628064502
python cli.py add-external --barcode 737628064502 --quantity 5 --price 3.50
```

## Tests

Run the automated tests:

```bash
pytest -q
```

## GitHub Actions

A CI workflow is included at `.github/workflows/pytest.yml` that runs the test
suite on push and pull request events.

## Final Submission

Submit the repository link below:

https://github.com/simonhiuhu-Leo/Inventory-management

This repo contains the full source code, setup instructions, CLI examples,
and automated tests required for the assignment.

## Change log

See [COMMITS.md](COMMITS.md) for the change log.
