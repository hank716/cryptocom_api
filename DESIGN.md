# 🧠 API Automation Design Document

## 🔖 Project Overview

This project is designed to validate the functionality and reliability of Crypto.com Exchange public APIs (REST and WebSocket) using Python and Behave. The framework ensures modularity, scalability, and maintainability.

## 🧪 Test Coverage

### ✅ Task 1: REST API — `public/get-candlestick`

**Test Focus:**
- Valid/invalid `instrument_name` and `timeframe`
- HTTP status codes
- Data structure and field validation
- Schema validation (using `jsonschema`)

### ✅ Task 2: WebSocket API — `book.{instrument_name}.{depth}`

**Test Focus:**
- Subscription confirmation
- Correct bid/ask depth and structure
- Error handling for invalid symbols
- High-frequency subscription tests

## 🔍 Assertion Strategy

- Status code checks
- JSON schema validation
- Logical checks for sorted timestamps and correct field values
- Bid/Ask field type verification (`float`)

## 🔁 Retry Strategy

- WebSocket auto reconnect with exponential backoff
- Re-subscription upon reconnect

## 🔐 Environment Configuration

All endpoints are configured via `.env`:

```ini
BASE_URL=https://api.crypto.com/v2
WS_URL=wss://stream.crypto.com/v2/market
```

## 🧱 Extensibility

- Supports adding new endpoints and test cases
- Can integrate database validation and performance tests
- Suitable for CI/CD pipelines (e.g., GitHub Actions)

## 📦 Tools

- Behave (BDD testing)
- requests, websocket-client
- jsonschema
- dotenv
- Allure / HTML reports
