# Test Design Overview

This document summarises the scenarios implemented in the Behave suites.

---

## REST: `public/get-candlestick`

| ID  | Description                                                   |
|-----|---------------------------------------------------------------|
| TC1 | Valid request returns multiple candlestick entries.           |
| TC2 | Different timeframe formats produce 1‑minute ordered data.    |
| TC3 | Each entry contains timestamp, open, high, low, close, volume |
| TC4 | `limit` parameter capped at 5000 records.                     |
| TC5 | Missing required parameter results in non‑zero error code.    |
| TC6 | Query for a specific time range returns only that range.      |
| TC7 | Invalid instrument name returns an error response.            |
| TC8 | Invalid timeframe string returns an error response.           |
| TC9 | Calling the endpoint without parameters is rejected.          |

## WebSocket: `book.{instrument_name}.{depth}`

| ID     | Description                                                                |
|--------|---------------------------------------------------------------------------|
| WS-TC1 | Successful subscription returns bid/ask book data.                         |
| WS-TC2 | Confirmation message is received for a valid subscription.                |
| WS-TC3 | Bid/ask values are numeric and timestamp fields are integers.             |
| WS-TC4 | Maximum depth subscription respects the requested depth limit.            |
| WS-TC5 | Rapid subscriptions to multiple instruments do not disconnect the client. |
| WS-TC6 | Subscribing to an inactive market keeps the connection open without data. |
| WS-TC7 | Invalid instrument name yields an error message.                           |
| WS-TC8 | Invalid depth value yields an error message.                               |
| WS-TC9 | No updates within timeout results in no disconnection or exception.       |

---

## Assertion and Retry Strategy

* Status code and error code validation.
* JSON schema checks on REST responses.
* Bid/ask data structure validation for WebSocket responses.
* Automatic reconnects with re-subscription on WebSocket failure.

Environment details are read from `.env` to support different targets.

