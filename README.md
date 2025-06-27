# 🧪 Crypto.com API Automation Framework


## 📑 Table of Contents

- [📚 Tech Stack](#-tech-stack)
- [📂 Project Structure](#-project-structure)
- [🚀 Features](#-features)
- [⚙️ Installation](#-installation)
- [🧪 Test Execution](#-test-execution)
- [📊 Test Coverage Summary](#-test-coverage-summary)
- [🗓️ API Response Structures](#-api-response-structures)
- [📊 Reports](#-reports)
- [🔄 CI/CD Pipeline](#-cicd-pipeline)
- [🌐 GitHub Pages](#-github-pages-deployment)
- [📢 Notes](#-notes)
- [🎯 Author](#-author)
- [🔝 Back to Top](#-table-of-contents)



## 📚 Tech Stack

- **Language**: Python 3.10+
- **Framework**: Behave (BDD)
- **Assertion/Validation**: JSONSchema, built-in assert
- **Reporting**: Allure + HTML static report
- **CI/CD**: GitHub Actions

---

[🔝 Back to Top](#-table-of-contents)


## 🗂 Project Structure

```
cryptocom_api/
├── .github/
│   └── workflows/
│       └── ci.yml                  # CI pipeline: install → test → report artifacts
├── features/                       # BDD feature & step files
│   ├── rest_api.feature            # REST scenarios
│   ├── websocket.feature           # WebSocket scenarios
│   └── steps/
│       ├── rest_steps.py           # implements REST steps
│       └── ws_steps.py             # implements WebSocket steps
│   └── environment.py          # hooks (before/after)
├── tests/
│   ├── data/
│   │   └── test_payloads.json      # data‑driven test inputs
│   └── utils/                      # reusable helper modules
│       ├── api_client.py           # REST client
│       ├── ws_client.py            # WebSocket wrapper (with reconnect)
│       ├── schema_validator.py     # JSON schema checks
│       └── logger.py               # consistent logging
├── scripts/
│   └── generate_report_index.py    # generates static HTML `docs/index.html`
├── reports/
│   └── allure-report/              # interactive Allure output
├── docs/                           # static HTML reports (from scripts)
├── .env                            # env config (e.g. base URL)
├── deploy_reports.sh               # deploy `docs/` to GitHub Pages or server
├── generate_allure_and_index.sh    # run tests → build Allure + docs
├── preview.sh                      # open `docs/index.html` locally
├── behave.ini                      # Behave configuration (tags, formatters)
├── requirements.txt                # Python dependencies
├── DESIGN.md                       # design doc + detailed test cases
└── README.md                       # (this file)
```

---

## ⚙️ Installation

### 🧪 Test Execution

1. 📦 Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. ▶ Run all BDD scenarios:

   ```bash
   behave
   ```

3. 🧪 Generate reports:

   ```bash
   bash generate_allure_and_index.sh
   ```

4. 🌐 Preview locally:

   ```bash
   bash preview.sh
   ```

---

[🔝 Back to Top](#-table-of-contents)


# 🧪 Crypto.com API Automation Framework

## 📑 Table of Contents

- [📚 Tech Stack](#-tech-stack)
- [📂 Project Structure](#-project-structure)
- [🚀 Features](#-features)
- [⚙️ Installation](#-installation)
- [🧪 Test Execution](#-test-execution)
- [📊 Test Coverage Summary](#-test-coverage-at-a-glance)
- [🗓️ API Response Structures](#-api-response-structures)
- [📊 Reports](#-how-to-view-allure-reports-locally)
- [🔄 CI/CD Pipeline](#-cicd)
- [🌐 GitHub Pages](#-github-pages-deployment)
- [📢 Notes](#-why-this-architecture-matters)
- [🎯 Author](#-author)
- [🔝 Back to Top](#-table-of-contents)


This is a robust, behavior‑driven API automation framework for Crypto.com Exchange **public APIs** — both **REST** and **WebSocket** — built with `Python` + `Behave`.

---

## 🚀 Features

- ✅ BDD‑style API testing via `.feature` scenarios
- 🔄 Supports both:
  - REST: `public/get-candlestick`
  - WebSocket: `book.{instrument_name}.{depth}`
- 🧩 Test coverage:
  - Positive / Negative / Boundary / Schema / Logical
- ✅ JSON schema validation with `jsonschema`
- 📊 Allure + static HTML reporting
- ⚙ Modular architecture (API & WS clients, schema validator, logger)
- 🔧 CI ready with GitHub Actions

---

[🔝 Back to Top](#-table-of-contents)


## 📊 Test Coverage Summary

| Area       | Endpoint                             | Coverage Types                                |
|------------|--------------------------------------|----------------------------------------------|
| REST API   | `/public/get-candlestick`           | Param validation, schema, chronological order |
| WebSocket  | `book.{instrument_name}.{depth}`    | Subscribe, error handling, reconnect, flow   |

See [DESIGN.md](./DESIGN.md) for full scenario breakdown.

---

## 🧱 Adding New Test Cases

1. **Add test input**  
   Extend `tests/data/test_payloads.json` with new JSON objects (structured by scenario type).  
   Example:
   ```json
   "new_candlestick_case": {
     "instrument_name": "ETH_USDT",
     "timeframe": "4h",
     "expect_status": 200
   }
   ```

2. **Edit or add `.feature` scenario**  
   Add Scenario to `*.feature`, referencing the new payload key:
   ```gherkin
   Scenario Outline: Test new timeframe
     Given I request candlestick "<key>"
     Then I should receive valid data
     Examples:
       | key                  |
       | new_candlestick_case |
   ```

3. **Implement or reuse step logic**  
   Step definitions in `rest_steps.py` or `ws_steps.py` will read from payloads and execute logic.  
   If needed, add new helper methods in `tests/utils/`.

4. **(Optional) Add schema**  
   If testing a brand-new endpoint or response type, update or add JSON schema in `schema_validator.py`.

5. **Run & verify**  
   Run `behave`, check reports under `reports/allure-results`, generate Allure & docs.

6. **Push to repo**  
   CI will auto-run tests and upload artifacts.

---

[🔝 Back to Top](#-table-of-contents)


## 🗓️ API Response Structures

### REST: `public/get-candlestick`
- Format: JSON
- Key fields:
  - `o`, `h`, `l`, `c`, `v`, `t`: open/high/low/close/volume/timestamp
- Ordered by `t` ascending

### WebSocket: `book.{instrument_name}.{depth}`
- Real-time stream of:
  - `asks`: [[price, quantity], ...]
  - `bids`: [[price, quantity], ...]
  - `timestamp`, `instrument_name`, `depth`

---

[🔝 Back to Top](#-table-of-contents)


## 📊 Reports

1. **Install Allure CLI**  
   - macOS: `brew install allure`  
   - Ubuntu/Fedora: `sudo apt install allure`  
   - Windows: Download from GitHub Releases, add `bin/` to `PATH`

2. **Ensure Behave emits results**  
   Confirm `behave.ini` contains:
   ```ini
   [behave.userdata]
   allure_report_dir = reports/allure-results
   ```

3. **Generate the report**  
   ```bash
   allure generate reports/allure-results -o reports/allure-report --clean
   ```

4. **Open it**  
   ```bash
   allure open reports/allure-report
   ```

5. **Quick method**  
   ```bash
   bash generate_allure_and_index.sh
   bash preview.sh
   ```

---

[🔝 Back to Top](#-table-of-contents)


## 🔄 CI/CD Pipeline

- GitHub Actions workflow (`ci.yml`) installs dependencies, runs tests and uploads report artifacts on every push or PR.
- You can enhance it to publish `docs/` to GitHub Pages via `deploy_reports.sh`.

---

[🔝 Back to Top](#-table-of-contents)


## 🌐 GitHub Pages Deployment

To deploy static HTML reports:

1. Ensure `docs/index.html` exists (via `generate_report_index.py`)
2. Enable GitHub Pages in repo settings, target `docs/` folder
3. Optionally automate via `deploy_reports.sh`
- 🔗 [Test report for this project](https://hank716.github.io/cryptocom_api/)

---

[🔝 Back to Top](#-table-of-contents)


## 📢 Notes

- **Readable** BDD scenarios separate logic from data
- **Scalable**: add new endpoints without breaking structure
- **Maintainable**: reusable utils + clean modular code
- **Traceable**: Allure reports + consistent logging help debug quickly

---

[🔝 Back to Top](#-table-of-contents)


## 🎯 Author

**Hank**  
🔗 [github.com/hank716](https://github.com/hank716)

[🔝 Back to Top](#-table-of-contents)
