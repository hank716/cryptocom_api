
from behave import given, then
import requests
import traceback
import allure
import json
import time

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


    if "start" in context.params and context.params["start"] == "NOW_MINUS_1H":
        now = int(time.time() * 1000)
        context.params["start"] = str(now - 60 * 60 * 1000)
    if "end" in context.params and context.params["end"] == "NOW":
        context.params["end"] = str(int(time.time() * 1000))

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
        if "tc1" in expected_lower:
            assert code == 200 and json_code == 0, "Expected success response"
            assert len(data) > 1, "Expected multiple candlestick entries"
            reason = f"Valid request returned {len(data)} candlesticks"

        elif "tc2" in expected_lower:
            timestamps = [int(d["t"]) for d in data[:10]]
            diffs = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
            assert all(abs(diff - 60000) <= 1000 for diff in diffs), f"Timestamps not 1-min apart: {diffs}"
            reason = "Timestamps are spaced ~60 seconds apart"

        elif "tc3" in expected_lower:
            required_keys = {"t", "o", "h", "l", "c", "v"}
            for i, d in enumerate(data[:5]):
                assert isinstance(d, dict), f"Candlestick at index {i} is not a dict"
                assert required_keys.issubset(d.keys()), f"Missing keys in candlestick {i}: {d}"
            reason = "Candlestick entries have required fields"

        elif "tc4" in expected_lower:
            assert len(data) <= 5000, f"Data too large: {len(data)} entries"
            reason = f"Data within 5000 entry limit: {len(data)}"

        elif "tc5" in expected_lower:
            assert json_code != 0, "Expected error due to missing required parameter"
            reason = f"API returned error as expected: JSON Code {json_code}"

        elif "tc6" in expected_lower:
            start = int(context.params.get("start", 0))
            end = int(context.params.get("end", 1e20))
            timestamps = [int(d["t"]) for d in data]
            assert all(start <= ts <= end for ts in timestamps), f"Timestamps out of range: {timestamps[:5]}"
            reason = f"All timestamps within range: {start} ~ {end}"

        elif "tc7" in expected_lower:
            assert json_code != 0, f"Expected error for invalid instrument name, got code=0"
            reason = f"Invalid instrument_name correctly returned error code: {json_code}"

        elif "tc8" in expected_lower:
            assert json_code != 0, f"Expected error for invalid timeframe format, got code=0"
            reason = f"Invalid timeframe format correctly returned error code: {json_code}"

        elif "tc9" in expected_lower:
            assert json_code != 0, f"Expected error for missing parameters, got code=0"
            reason = f"Missing parameters correctly returned error code: {json_code}"

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
