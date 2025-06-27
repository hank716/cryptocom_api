from behave import given, then
import requests
import traceback
import allure

@given('REST test input "{input}"')
def step_given_rest_input(context, input):
    context.params = {}
    input = input.strip()

    with allure.step(f"Parse input: {input}"):
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

    with allure.step("Send REST API request"):
        context.response = requests.get(url, params=context.params)
        allure.attach(
            f"URL: {url}\nParams: {context.params}",
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
    json_code = context.response.json().get("code", None)
    expected_lower = expected.lower()

    logcat_text = f"""REST Assertion Evaluation:
- Expected: {expected}
- HTTP Status: {code}
- JSON Code: {json_code}
- Response Body: {context.response.text[:1000]}
"""
    allure.attach(logcat_text, name="Assertion Context", attachment_type=allure.attachment_type.TEXT)

    try:
        with allure.step("Evaluate REST response"):
            if "code != 0" in expected_lower or "error message" in expected_lower:
                assert json_code != 0, f"Expected API error code, got code=0 and HTTP {code}"
            elif "200" in expected_lower:
                assert code == 200 and json_code == 0, f"Expected success, got HTTP {code}, code={json_code}"

        allure.attach(
            f"Assertion passed.\nStatus: {code}\nJSON Code: {json_code}\nResponse: {context.response.text[:1000]}",
            name="REST Assertion Summary",
            attachment_type=allure.attachment_type.TEXT
        )

    except Exception as e:
        allure.attach(
            f"Exception: {str(e)}\nTraceback:\n{traceback.format_exc()}",
            name="REST Assertion Error",
            attachment_type=allure.attachment_type.TEXT
        )
        raise
