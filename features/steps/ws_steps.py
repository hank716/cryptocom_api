
from behave import given, then
import websocket
import json
import threading
import time
import traceback
import allure

def is_error_response(context):
    timeout = time.time() + 5
    while time.time() < timeout:
        if context.ws_error:
            return True
        for m in context.ws_messages:
            if "error" in m or m.get("code", 0) != 0:
                return True
        time.sleep(0.5)
    for m in context.ws_messages:
        if "result" in m and m["result"].get("status") == "success":
            has_data_push = any(
                "method" in x or ("result" in x and "data" in x["result"])
                for x in context.ws_messages
            )
            if not has_data_push:
                return True
    return False

@given('WS test input "{input}"')
def step_given_ws_input(context, input):
    context.params = {}
    if input.startswith("book."):
        parts = input.split(".")
        if len(parts) == 3:
            context.params["instrument_name"] = parts[1]
            context.params["depth"] = parts[2]
        else:
            raise ValueError("Invalid topic format. Expected: book.{instrument_name}.{depth}")
    else:
        for pair in input.split(','):
            if '=' in pair:
                k, v = pair.strip().split('=')
                context.params[k.strip()] = v.strip()
            elif pair.strip().isdigit():
                context.params["depth"] = pair.strip()
            else:
                context.params["instrument_name"] = pair.strip()

    if "instrument_name" not in context.params:
        context.params["instrument_name"] = "BTC_USDT"
    if "depth" not in context.params:
        context.params["depth"] = "10"

    if "tc4" not in context.scenario.name.lower():  # Symbols are restricted only if they are not TC4
        allowed_symbols = {"BTC_USDT", "ETH_USDT", "CRO_USDT"}
        if context.params["instrument_name"] not in allowed_symbols:
            raise ValueError(f"Unsupported instrument_name: {context.params['instrument_name']}. Allowed: {allowed_symbols}")

    context.ws_messages = []
    context.ws_error = None
    context.ws_closed = False

    def on_message(ws, message):
        context.ws_messages.append(json.loads(message))

    def on_open(ws):
        subscription = {
            "method": "subscribe",
            "params": {
                "channels": [f"book.{context.params['instrument_name']}.{context.params['depth']}"]
            },
            "id": 1
        }
        ws.send(json.dumps(subscription))
        allure.attach(json.dumps(subscription, indent=2), name="Sent Subscription", attachment_type=allure.attachment_type.JSON)

    def on_error(ws, error):
        context.ws_error = str(error)

    def on_close(ws, *_):
        context.ws_closed = True

    context.ws = websocket.WebSocketApp(
        context.ws_url,
        on_message=on_message,
        on_open=on_open,
        on_error=on_error,
        on_close=on_close
    )

    thread = threading.Thread(target=context.ws.run_forever)
    thread.daemon = True
    thread.start()

    timeout = 20
    start_time = time.time()
    while time.time() - start_time < timeout:
        if context.ws_messages or context.ws_error:
            break
        time.sleep(0.5)

# === Modular Assertions for WS-TC1 ~ WS-TC9 ===

def assert_ws_tc1_subscription(context):
    assert any("result" in m or "method" in m for m in context.ws_messages), "No subscription confirmation found"

def assert_ws_tc2_orderbook_present(context):
    book_data = None
    end_time = time.time() + 10
    while time.time() < end_time:
        for m in context.ws_messages:
            if "result" in m and "data" in m["result"]:
                book_data = m["result"]["data"][0]
                break
        if book_data:
            break
        time.sleep(0.5)
    assert book_data, "No orderbook data with bids/asks found"
    context.book_data = book_data

def assert_ws_tc3_validate_format(context):
    if not hasattr(context, 'book_data'):
        assert_ws_tc2_orderbook_present(context)
    book_data = getattr(context, "book_data", None)
    if not book_data:
        for m in context.ws_messages:
            if "result" in m and "data" in m["result"]:
                book_data = m["result"]["data"][0]
                break
    assert book_data, "No book data to validate format"
    assert isinstance(book_data.get("t", 0), int)
    assert all(isinstance(float(bid[0]), float) for bid in book_data.get("bids", []))
    assert all(isinstance(float(ask[0]), float) for ask in book_data.get("asks", []))

def assert_ws_tc4_error_expected(context):
    assert is_error_response(context), "Expected error response but none found"

def assert_ws_tc5_depth_limit(context):
    if not hasattr(context, 'book_data'):
        assert_ws_tc2_orderbook_present(context)
    book_data = getattr(context, "book_data", None)
    assert book_data, "Missing book_data"
    assert len(book_data["bids"]) <= int(context.params["depth"])
    assert len(book_data["asks"]) <= int(context.params["depth"])

def assert_ws_tc6_bid_ask_not_empty(context):
    if not hasattr(context, 'book_data'):
        assert_ws_tc2_orderbook_present(context)
    book_data = getattr(context, "book_data", None)
    assert book_data, "Missing book_data"
    assert len(book_data["bids"]) > 0 and len(book_data["asks"]) > 0, "Bid or ask list is empty"

def assert_ws_tc7_price_quantity_type(context):
    if not hasattr(context, 'book_data'):
        assert_ws_tc2_orderbook_present(context)
    book_data = getattr(context, "book_data", None)
    for bid in book_data.get("bids", []):
        assert isinstance(float(bid[0]), float)
        assert isinstance(float(bid[1]), float)
    for ask in book_data.get("asks", []):
        assert isinstance(float(ask[0]), float)
        assert isinstance(float(ask[1]), float)

def assert_ws_tc8_timestamp_monotonic(context):
    timestamps = []
    for m in context.ws_messages:
        if "result" in m and "data" in m["result"]:
            for entry in m["result"]["data"]:
                timestamps.append(entry.get("t"))
    assert all(timestamps[i] <= timestamps[i+1] for i in range(len(timestamps)-1)), "Timestamps not monotonic"

def assert_ws_tc9_duplicate_subscription(context):
    ids = [m.get("id") for m in context.ws_messages if "id" in m]
    assert len(ids) == len(set(ids)), "Duplicate subscription IDs detected"

@then('WS expected result should be "{expected}"')
def step_then_ws_expected(context, expected):
    expected = expected.lower()

    try:
        if "tc1" in expected:
            assert_ws_tc1_subscription(context)
        if "tc2" in expected:
            assert_ws_tc2_orderbook_present(context)
        if "tc3" in expected:
            assert_ws_tc3_validate_format(context)
        if "tc4" in expected:
            assert_ws_tc4_error_expected(context)
        if "tc5" in expected:
            assert_ws_tc5_depth_limit(context)
        if "tc6" in expected:
            assert_ws_tc6_bid_ask_not_empty(context)
        if "tc7" in expected:
            assert_ws_tc7_price_quantity_type(context)
        if "tc8" in expected:
            assert_ws_tc8_timestamp_monotonic(context)
        if "tc9" in expected:
            assert_ws_tc9_duplicate_subscription(context)

        allure.attach("✅ WS Assertion Passed", name="WS Assertion", attachment_type=allure.attachment_type.TEXT)
    except Exception as e:
        allure.attach(f"❌ WS Assertion Failed\nReason: {str(e)}", name="WS Assertion Error", attachment_type=allure.attachment_type.TEXT)
        traceback.print_exc()
        raise
    finally:
        if context.ws:
            context.ws.close()
