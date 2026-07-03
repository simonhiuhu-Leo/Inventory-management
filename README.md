# Inventory Management System — a short story

Once upon a time there was a tiny inventory service. It kept a list of things, could
ask an external food database for product details, and let a curious user add, edit,
or remove items. This repository contains that little service along with a CLI and
tests that read like short scenes.

## Highlights

- CRUD inventory endpoints and a friendly CLI.
- Search by `name` or `barcode`.
- Enrich items using the OpenFoodFacts API.
- Tests written to describe user stories and guard behavior with precision.

## Quickstart

Copy these commands into a terminal in the repository root to get running.

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install required packages:

```bash
pip install -r requirements.txt
```

Run the API locally:

```bash
python app.py
```

The service listens on `http://127.0.0.1:5000` by default.

## CLI examples (short scenes)

```bash
python cli.py list
python cli.py add "Garden Apple" --barcode 12345 --quantity 10 --price 1.99
python cli.py get 1
python cli.py update 1 --quantity 12
python cli.py delete 1
python cli.py fetch --barcode 737628064502
python cli.py add-external --barcode 737628064502 --quantity 5 --price 3.50
```

## Tests — run the story-driven suite

Our tests are written as short narratives that make each scenario obvious. Run them with:

```bash
pytest -q
```

## Commit history (narrative)

See the [commit story](COMMITS.md) for step-by-step human-friendly change notes.

## Contributing

If you'd like commits written in a particular voice (short, poetic, or plain), say the word
and I will continue in that style.
