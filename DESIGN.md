# 🧠 API Automation Design Document

## 🔖 Overview

This project automates testing of the Crypto.com Exchange public APIs:

- ✅ REST: `public/get-candlestick`
- ✅ WebSocket: `book.{instrument_name}.{depth}`

It uses the BDD (Behavior-Driven Development) approach with `Behave`, allowing test cases to be defined in natural language and implemented in Python steps.

---

## 📐 Test Case Design Principles

Followed several principles for test case design:

- **Data-driven Testing**: test payloads are stored in JSON for parameterized execution
- **Boundary Value Analysis**: especially for numeric fields such as depth or granularity
- **Negative Testing**: validate error handling for invalid symbols or timeframes
- **Schema Validation**: all responses are checked against expected JSON schemas
- **Retry Logic**: especially for WebSocket connections

---

## ✅ Task 1 — REST API: `/public/get-candlestick`

### Test Scenarios

| Scenario Description                           | Input                         | Expected Outcome                          |
|------------------------------------------------|-------------------------------|-------------------------------------------|
| Valid instrument + valid timeframe             | BTC_USDT, 1m                  | 200 OK + Valid JSON                       |
| Invalid instrument name                        | FAKE_COIN, 1m                 | 200 OK + Empty or error response          |
| Invalid timeframe format                       | BTC_USDT, fake_time           | 400 Bad Request or handled response       |
| Schema validation                              | Valid inputs                  | Fields match expected structure           |
| Timestamp ordering check                       | Valid inputs                  | Data sorted chronologically               |

---

## ✅ Task 2 — WebSocket: `book.{instrument_name}.{depth}`

### Test Scenarios

| Scenario Description                           | Input                         | Expected Outcome                          |
|------------------------------------------------|-------------------------------|-------------------------------------------|
| Subscribe with valid symbol + depth            | BTC_USDT, 10                  | Subscription confirmed + book snapshot    |
| Invalid symbol name                            | FAKE_COIN, 10                 | Error message or failure event            |
| Depth too large                                | BTC_USDT, 100000              | Rejection or fallback response            |
| Field type validation                          | Any valid book update         | All bids/asks are floats, sorted          |
| Reconnect and retry                            | Disconnect mid-stream         | Auto reconnect and re-subscribe           |

---

## 🔍 Assertion Strategy

- Status Code (REST): 200, 400, etc.
- WebSocket message type matching: `book`, `error`, `subscription`
- JSON schema: use `jsonschema` to validate payload structure
- Field checks:
  - `instrument_name` is a valid string
  - `depth` is an integer
  - `price` and `quantity` are float

---

## 🔁 WebSocket Retry Strategy

- Auto reconnect on `on_close` with exponential backoff
- Re-subscribe using stored instrument + depth
- Ensure data resumption and message integrity

---

## 📊 Reporting

- Allure used for visual test result reporting
- `generate_report_index.py` builds an HTML index for static viewing

---

## 🔧 Maintainability

- Modular `api_client.py` and `ws_client.py` for reuse
- New test cases can be added by updating `test_payloads.json` + `.feature` files



---

## 📋 Detailed Test Cases

### ✅ REST API: `/public/get-candlestick`

| TC#  | Description                                | Type       | Notes                                                  |
|------|--------------------------------------------|------------|--------------------------------------------------------|
| TC01 | Valid instrument and timeframe             | Positive   | BTC_USDT, 1m — Expect 200 and candlestick data         |
| TC02 | Valid instrument with daily timeframe      | Positive   | BTC_USDT, 1d — Verify aggregation handling             |
| TC03 | Invalid instrument name                    | Negative   | FAKE_COIN — Expect error or empty data                |
| TC04 | Invalid timeframe format                   | Negative   | Use string like "abc" — Expect validation error       |
| TC05 | Missing instrument_name                    | Negative   | Omit parameter — Should return 400                    |
| TC06 | Missing timeframe                          | Negative   | Omit parameter — Should return 400                    |
| TC07 | Schema validation                          | Schema     | Validate response matches expected candlestick format |
| TC08 | Chronological ordering                     | Logical    | Ensure timestamps are in ascending order              |
| TC09 | Future date request                        | Boundary   | Query future time — Should return no data             |

### ✅ WebSocket API: `book.{instrument_name}.{depth}`

| TC#  | Description                                | Type       | Notes                                                  |
|------|--------------------------------------------|------------|--------------------------------------------------------|
| TC10 | Subscribe to valid book                    | Positive   | BTC_USDT, depth=10 — Expect confirmation + data        |
| TC11 | Invalid instrument name                    | Negative   | FAKE_COIN — Expect subscription failure or error msg   |
| TC12 | Invalid depth format                       | Negative   | Use non-integer string — Expect error or ignore        |
| TC13 | Excessively large depth                    | Boundary   | depth=999999 — Should be capped or rejected            |
| TC14 | Field type and structure check             | Schema     | Ensure bids/asks are float, properly nested            |
| TC15 | Timestamp ordering                         | Logical    | Ensure new snapshots respect ordering rules            |
| TC16 | Unsubscribe and re-subscribe               | Functional | Test toggle logic and stability                        |
| TC17 | Network disconnection and retry            | Resilience | Should reconnect and resume subscription               |
| TC18 | High-frequency instrument switching        | Stress     | Rapid subscription change — Check socket stability     |


---

## 🚧 Additional Design Considerations

### 🔄 CI/CD Integration
This project includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that automatically:
- Installs dependencies
- Runs all Behave test suites
- Uploads test reports as build artifacts
- Can be extended to deploy test reports via GitHub Pages

### 📁 Utilities & Modularity
Reusable Python modules under `tests/utils/` include:
- `api_client.py`: Base client for REST interactions
- `ws_client.py`: WebSocket manager with reconnect logic
- `schema_validator.py`: JSON schema validation helper
- `logger.py`: Unified logging format

These promote single-responsibility and reduce duplication.

### 📊 Reporting Automation
Test results are enhanced with:
- **Allure reporting** for detailed results and attachments
- `scripts/generate_report_index.py` auto-generates a static HTML index for local viewing
