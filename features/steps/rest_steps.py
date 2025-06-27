from behave import given, then
import requests

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

    # Auto-fill instrument_name if missing
    if "instrument_name" not in context.params and "timeframe" in context.params:
        context.params["instrument_name"] = "BTC_USDT"

    context.base_url = context.base_url or "https://api.crypto.com/v2"
    url = f"{context.base_url}/public/get-candlestick"
    context.response = requests.get(url, params=context.params)
    print(f"[REST] Request to: {url} with params={context.params}")
    print(f"[REST] Response: {context.response.status_code}, {context.response.text[:300]}")

@then('REST expected result should be "{expected}"')
def step_then_rest_expected(context, expected):
    code = context.response.status_code
    json_code = context.response.json().get("code", None)
    expected_lower = expected.lower()

    print(f"[ASSERT] Status: {code}, JSON Code: {json_code}, Expected: {expected}")

    if "code != 0" in expected_lower or "error message" in expected_lower or "400" in expected_lower:
        assert json_code != 0, f"Expected API error code, got code=0 and HTTP {code}"
    elif "200" in expected_lower:
        assert code == 200 and json_code == 0, f"Expected success, got HTTP {code}, code={json_code}"
