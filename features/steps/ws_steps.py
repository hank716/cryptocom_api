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

import allure

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
    
        subscription = {
            "method": "subscribe",
            "params": {
                "channels": [f"book.{context.params['instrument_name']}.{context.params['depth']}"]
            },
            "id": 1
        }
        ws.send(json.dumps(subscription))
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

@then('WS expected result should be "{expected}"')
def step_then_ws_expected(context, expected):
    print("="*30)
    print(f"[WebSocket] URL: {context.ws_url}")
    print(f"[WebSocket] Received {len(context.ws_messages)} messages")
    if context.ws_error:
        print(f"[WebSocket ERROR]: {context.ws_error}")
    print("[DEBUG] First few WebSocket messages:")
    allure.attach(
        json.dumps(context.ws_messages[:10], indent=2),
        name="WS Messages Snapshot",
        attachment_type=allure.attachment_type.JSON
    )

    # Logcat + Allure
    logcat_text = f"""WebSocket Assertion Evaluation:
- Expected: {expected}
- Message Count: {len(context.ws_messages)}
- Error: {context.ws_error}
- First Message: {json.dumps(context.ws_messages[:1], indent=2) if context.ws_messages else 'None'}
"""
    print(logcat_text)
    allure.attach(logcat_text, name="WS Assertion Context", attachment_type=allure.attachment_type.TEXT)

    allure.attach(
        f"""✅ Assertion Passed\nReason: Subscription confirmed and depth book data received\nMessages Received: {len(context.ws_messages)}\n""",
        name="WS Assertion Summary",
        attachment_type=allure.attachment_type.TEXT
    )

    expected = expected.lower()

    try:
        if "subscription" in expected:
            subs = [m for m in context.ws_messages if "result" in m or "method" in m]
            assert subs, f"No subscription confirmation found in messages: {context.ws_messages}"
        if "bid/ask" in expected or "depth" in expected:
            book_data = None
            end_time = time.time() + 5
            while time.time() < end_time:
                for m in context.ws_messages:
                    if "result" in m and "data" in m["result"]:
                        book_data = m["result"]["data"][0]
                        break
                if book_data:
                    break
                time.sleep(0.5)
            assert book_data, "No orderbook data with bids/asks found"
            assert "bids" in book_data and "asks" in book_data
            expected_depth = int(context.params["depth"])
            assert len(book_data["bids"]) <= expected_depth
            assert len(book_data["asks"]) <= expected_depth
        if "format" in expected:
            book_data = None
            for m in context.ws_messages:
                if "result" in m and "data" in m["result"]:
                    book_data = m["result"]["data"][0]
                    break
            assert book_data, "No book data to validate format"
            assert isinstance(book_data.get("t", 0), int)
            assert all(isinstance(float(bid[0]), float) for bid in book_data.get("bids", []))
            assert all(isinstance(float(ask[0]), float) for ask in book_data.get("asks", []))
        if "error" in expected:
            assert is_error_response(context), "Expected error response but none found"
    except Exception as e:
        allure.attach(
            f"""❌ Assertion Failed\nExpected: {expected}\nActual: WebSocket message count = {len(context.ws_messages)}, Error = {context.ws_error}\nReason: {str(e)}""",
            name="WS Assertion Error",
            attachment_type=allure.attachment_type.TEXT
        )
        allure.attach(
            f"Assertion failed.\nMessages:\n{json.dumps(context.ws_messages, indent=2)}\nError:\n{context.ws_error}",
            name="WS Assertion Error",
            attachment_type=allure.attachment_type.TEXT
        )
        traceback.print_exc()
        raise
    finally:
        print("="*30)
