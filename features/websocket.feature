# Most scenarios use the same WebSocket channel input.
# We vary the assertions (Then step) to test different logic aspects on the same stream.

Feature: WebSocket Book Channel Tests

  Scenario: WS-TC1 - Validate subscription success
    Given WS test input "BTC_USDT, depth=10"
    Then WS expected result should be "TC1"

  Scenario: WS-TC2 - Validate orderbook data presence
    Given WS test input "BTC_USDT, depth=10"
    Then WS expected result should be "TC2"

  Scenario: WS-TC3 - Validate data field types
    Given WS test input "BTC_USDT, depth=10"
    Then WS expected result should be "TC3"

  Scenario: WS-TC4 - Validate error handling
    Given WS test input "INVALID_SYMBOL, depth=10"
    Then WS expected result should be "TC4"

  Scenario: WS-TC5 - Validate orderbook depth limit
    Given WS test input "BTC_USDT, depth=10"
    Then WS expected result should be "TC5"

  Scenario: WS-TC6 - Validate bid/ask data not empty
    Given WS test input "BTC_USDT, depth=10"
    Then WS expected result should be "TC6"

  Scenario: WS-TC7 - Validate bid/ask price and quantity types
    Given WS test input "BTC_USDT, depth=10"
    Then WS expected result should be "TC7"

  Scenario: WS-TC8 - Validate timestamp order
    Given WS test input "BTC_USDT, depth=10"
    Then WS expected result should be "TC8"

  Scenario: WS-TC9 - Validate no duplicate subscription IDs
    Given WS test input "book.BTC_USDT.10"
    Then WS expected result should be "TC9"
