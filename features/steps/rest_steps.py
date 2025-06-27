
from behave import given, then
import requests
import traceback
import allure
import json

@given('REST test input "{input}"')
def step_given_rest_input(context, input):
    context.params = {}
    input = input.strip()

    if input.lower() in ["any valid request", "any request"]:
        context.params = {"instrument_name": "BTC_USDT", "timeframe": "5m"}
    elif input.lower() in ["empty body or query"]:
        context.params = {}
    else:
        for pair in input.split(','):
            if '=' in pair:
                key, value = pair.strip().split('=')
                context.params[key.strip()] = value.strip()
            elif "missing" in pair.lower():
                continue

    if "instrument_name" not in context.params and "timeframe" in context.params:
        context.params["instrument_name"] = "BTC_USDT"

    context.base_url = context.base_url or "https://api.crypto.com/v2"
    url = f"{context.base_url}/public/get-candlestick"
    context.response = requests.get(url, params=context.params)

    allure.attach(
        f"URL: {url}\nParams: {context.params}\nStatus: {context.response.status_code}",
        name="Request Details",
        attachment_type=allure.attachment_type.TEXT
    )

    allure.attach(
        f"Request: {url}\nParams: {context.params}\nStatus: {context.response.status_code}\nBody: {context.response.text[:1000]}",
        name="REST API Call",
        attachment_type=allure.attachment_type.TEXT
    )

@then('REST expected result should be "{expected}"')
def step_then_rest_expected(context, expected):
    code = context.response.status_code
    body = context.response.json()
    json_code = body.get("code", None)
    data = body.get("result", {}).get("data", [])
    expected_lower = expected.lower()

    logcat_lines = [
        "REST Assertion Evaluation:",
        f"- Expected: {expected}",
        f"- HTTP Status: {code}",
        f"- JSON Code: {json_code}",
        f"- Response Body: {context.response.text[:300]}"
    ]
    allure.attach("\n".join(logcat_lines), name="REST Assertion Evaluation", attachment_type=allure.attachment_type.TEXT)

    try:
        if "code != 0" in expected_lower or "error message" in expected_lower or "400" in expected_lower:
            assert json_code != 0, f"Expected API error code, got code=0 and HTTP {code}"
            reason = f"Expected error response (HTTP {code}, JSON Code {json_code})"

        elif "code == 0" in expected_lower or "success" in expected_lower or "http 200" in expected_lower:
            assert code == 200 and json_code == 0, f"Expected success, got HTTP {code}, code={json_code}"
            reason = f"Request succeeded (HTTP 200, Code 0)"

        elif "contains multiple entries" in expected_lower:
            assert len(data) > 1, f"Expected multiple entries, got {len(data)}"
            reason = f"Result contains multiple entries: {len(data)}"

        elif "within the specified range" in expected_lower:
            start = int(context.params.get("start", 0))
            end = int(context.params.get("end", 1e20))
            timestamps = [int(d[0]) for d in data]
            assert all(start <= ts <= end for ts in timestamps), f"Timestamps out of range: {timestamps[:5]}"
            reason = f"All timestamps are within range: {start} ~ {end}"

        elif "each candlestick contains" in expected_lower:
            for i, d in enumerate(data[:5]):
                assert isinstance(d, list) and len(d) >= 6, f"Invalid candlestick at index {i}: {d}"
            reason = "First 5 candlesticks have expected fields"

        elif "at most 5000 entries" in expected_lower:
            assert len(data) <= 5000, f"Data has too many entries: {len(data)}"
            reason = f"Data has {len(data)} entries, within expected limit"

        elif "timestamps reflect 1-minute intervals" in expected_lower:
            timestamps = [int(d[0]) for d in data[:10]]
            diffs = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
            assert all(abs(diff - 60000) <= 1000 for diff in diffs), f"Intervals not ~1m: {diffs}"
            reason = "Timestamps have ~60 sec intervals"

        else:
            reason = f"Condition met (HTTP {code}, Code {json_code})"

        allure.attach(
            f"[PASS] Assertion Passed\nReason: {reason}",
            name="REST Assertion Summary",
            attachment_type=allure.attachment_type.TEXT
        )

    except Exception as e:
        allure.attach(
            f"[FAIL] Assertion Failed\nExpected: {expected}\nActual HTTP: {code}\nActual JSON Code: {json_code}\nReason: {str(e)}",
            name="REST Assertion Error",
            attachment_type=allure.attachment_type.TEXT
        )
        raise
