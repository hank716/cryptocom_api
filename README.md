# Crypto.com API Test Framework

This repository contains an automated test suite for the public Crypto.com Exchange API. The tests cover both REST and WebSocket endpoints using **Behave** and generate Allure/HTML reports.

---

## Project Structure

```
cryptocom_api/
├── features/                # BDD feature files and step code
│   ├── rest_api.feature     # Scenarios for REST endpoints
│   ├── websocket.feature    # Scenarios for WebSocket endpoints
│   ├── steps/               # Step implementations
│   └── environment.py       # Hooks and environment setup
├── tests/                   # Helper utilities and sample data
│   └── data/test_payloads.json
├── DESIGN.md                # Test design and case overview
├── requirements.txt         # Python dependencies
└── README.md                # This document
```

---

## Setup

1. **Create a virtual environment** (conda or venv).
2. Install dependencies from `requirements.txt`.
3. Define `BASE_URL` and `WS_URL` in a `.env` file.

```
BASE_URL=https://api.crypto.com/v2
WS_URL=wss://stream.crypto.com/v2/market
```

---

## Running the Tests

Run all scenarios:

```
behave
```

Run a specific feature file:

```
behave features/rest_api.feature
behave features/websocket.feature
```

After execution, open `reports/index.html` to view the report.

---

## Feature Summary

The framework verifies the public candlestick REST API and the order book WebSocket channel.

### REST Scenarios

1. **TC1** – Valid request returns multiple candlesticks.
2. **TC2** – Handles various timeframe formats.
3. **TC3** – Each candlestick has timestamp, open, high, low, close and volume fields.
4. **TC4** – Max limit request returns at most 5000 records.
5. **TC5** – Missing required parameter triggers an error response.
6. **TC6** – Query by specific time range returns data within that range.
7. **TC7** – Invalid instrument name returns an error.
8. **TC8** – Invalid timeframe format returns an error.
9. **TC9** – No parameters provided returns an error code.

### WebSocket Scenarios

1. **WS‑TC1** – Successful subscription returns order book data.
2. **WS‑TC2** – Subscription confirmation message is verified.
3. **WS‑TC3** – Bid/ask values are numeric and timestamp is integer.
4. **WS‑TC4** – Depth limit respected for maximum depth subscription.
5. **WS‑TC5** – Multiple rapid subscriptions do not disconnect the client.
6. **WS‑TC6** – Subscribing to an inactive market keeps the connection stable.
7. **WS‑TC7** – Invalid instrument name returns an error message.
8. **WS‑TC8** – Invalid depth value returns an error message.
9. **WS‑TC9** – No updates after timeout are handled without exceptions.

---

## CI Example

A minimal GitHub Actions job might look like:

```yaml
- name: Run Behave tests
  run: behave

- name: Archive report
  uses: actions/upload-artifact@v3
  with:
    name: test-report
    path: reports/
```

---

This project aims to provide clear examples for exercising Crypto.com public APIs. Feel free to extend the scenarios or integrate new endpoints as required.
