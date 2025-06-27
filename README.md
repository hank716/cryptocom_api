# 🧪 Crypto.com API Automation Framework

This project is an end-to-end test automation framework for validating the public Crypto.com Exchange API — both REST and WebSocket endpoints — with extensibility and maintainability in mind.

---

## 📌 Features

- ✅ Support for **REST API** testing: `public/get-candlestick`
- ✅ Support for **WebSocket API** testing: `book.{instrument_name}.{depth}`
- 🧠 Covers multiple test types: positive, negative, boundary, and schema validation
- 🛠️ Built with **Python + Behave** (BDD-style testing)
- 📊 Integrated with **Allure / HTML reports**
- 🔁 Retry and reconnect logic for WebSocket
- ☁️ Ready for GitHub Actions CI/CD

---

## 🗂️ Project Structure

```bash
crypto_api_automation/
├── README.md                # Project instructions (this file)
├── DESIGN.md                # Test strategy and design
├── requirements.txt         # Python dependencies
├── behave.ini               # Behave config
├── features/
│   ├── environment.py       # Global hooks (setup/teardown)
│   ├── steps/
│   │   ├── rest_steps.py    # Step definitions for REST
│   │   └── ws_steps.py      # Step definitions for WebSocket
│   ├── rest_api.feature     # Feature file for REST testing
│   └── websocket.feature    # Feature file for WebSocket testing
├── tests/
│   ├── data/
│   │   └── test_payloads.json   # Input data for testing
│   ├── utils/
│   │   ├── api_client.py        # Wrapper for REST calls
│   │   ├── ws_client.py         # WebSocket client handler
│   │   ├── schema_validator.py # JSON Schema validator
│   │   └── logger.py            # Custom logging utility
├── reports/                # Allure / HTML test report output
```

---

## 🚀 Quick Start

### 1. Create Environment & Install Dependencies

```bash
# Using conda
conda create -n crypto_api_test python=3.11
conda activate crypto_api_test

# Install required packages
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file at the root:

```ini
BASE_URL=https://api.crypto.com/v2
WS_URL=wss://stream.crypto.com/v2/market
```

---

## 🧪 How to Run Tests

### ✅ Run REST API Tests

```bash
behave features/rest_api.feature
```

### ✅ Run WebSocket API Tests

```bash
behave features/websocket.feature
```

### 📊 View HTML Report

After test execution:

```bash
open reports/index.html  # macOS
# or
xdg-open reports/index.html  # Linux
```

---

## 🧠 Test Coverage & Design Summary

### REST API: `public/get-candlestick`

- Status Code validation
- Schema validation via `jsonschema`
- Data validation: timestamp order, values
- Negative test: invalid instrument/timeframe
- Boundary test: max time window

### WebSocket API: `book.{instrument_name}.{depth}`

- Subscription confirmation check
- Bid/ask structure and depth validation
- Malformed topic handling
- High frequency & reconnect scenarios

---

## 🔧 Tools Used

| Tool              | Purpose                         |
|-------------------|----------------------------------|
| `Behave`          | BDD test definition & execution |
| `requests`        | REST API client                 |
| `websocket-client`| WebSocket connection            |
| `jsonschema`      | Response schema validation      |
| `dotenv` / `os`   | Env variable management         |
| `Allure` / `pytest-html` | Report generation         |

---

## ⚙️ CI/CD Pipeline (GitHub Actions)

Example workflow step:

```yaml
- name: Run REST & WS API Tests
  run: behave features/

- name: Upload Allure Report
  uses: actions/upload-artifact@v3
  with:
    name: test-report
    path: reports/
```

---

## 📌 Future Enhancements

- ✅ Add support for private/secured API endpoints
- ✅ Add database data verification layer
- ✅ Multi-env support (Staging/Prod)
- ✅ Performance/Load testing via Locust or K6
- ✅ Daily scheduled health check pipelines

---

## 🧠 Author's Note

This framework is designed to be beginner-friendly yet scalable for teams. Feel free to fork and adapt it to suit your environment.
