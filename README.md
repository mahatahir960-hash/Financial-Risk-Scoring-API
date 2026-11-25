# financial-risk-scoring-api

Serve financial risk scores over a local HTTP API.

## What it demonstrates
A focused, runnable proof of concept aligned with data science, analytics, and model governance. Uses **synthetic data only**; no employer data, private datasets, or claims of production deployment.

## Setup
```bash
python -m venv .venv
# Activate your virtual environment, then:
pip install -r requirements.txt
```

## Run
```bash
python -m src.main  # starts local API on port 8080
```

## Tests
```bash
python -m pytest -q
```

## Notes
- Reproducible examples use fixed random seeds where applicable.
- This is a portfolio-sized baseline. Adapt the schema, thresholds, validation, and deployment controls before real-world use.
- All examples are illustrative, not clinical or financial advice.

Example request (in another terminal):
```bash
curl -X POST http://127.0.0.1:8080/score -H 'Content-Type: application/json' -d '{"features":[0,1,0,1,0,1,0,1]}'
```
