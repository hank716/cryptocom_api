Feature: WebSocket API: book.{instrument_name}.{depth}

  Scenario: WS-TC1 - Successful subscription returns order book
    Given WS test input "BTC_USDT, depth=10"
    Then WS expected result should be "subscription confirmed with bid/ask data received"

  Scenario: WS-TC2 - Verify subscription confirmation message
    Given WS test input "valid channel format"
    Then WS expected result should be "successful subscription message received"

  Scenario: WS-TC3 - Validate data field types
    Given WS test input "price/quantity as float, timestamp as integer"
    Then WS expected result should be "data format is valid"

  Scenario: WS-TC4 - Subscribe with maximum depth
    Given WS test input "depth=150"
    Then WS expected result should be "number of bid/ask matches depth"

  Scenario: WS-TC5 - Rapid multiple subscriptions
    Given WS test input "subscribe to multiple instruments rapidly"
    Then WS expected result should be "all subscriptions succeed without disconnection"

  Scenario: WS-TC6 - Subscribe to inactive market with no real-time data
    Given WS test input "CRO_ETH, depth=10"
    Then WS expected result should be "no data received but connection remains stable"

  Scenario: WS-TC7 - Subscribe with invalid instrument name
    Given WS test input "book.INVALID_COIN.10"
    Then WS expected result should be "error message returned"

  Scenario: WS-TC8 - Subscribe with invalid depth value
    Given WS test input "depth='abc' or -10"
    Then WS expected result should be "error message returned"

  Scenario: WS-TC9 - No updates received after timeout
    Given WS test input "any low-volume instrument"
    Then WS expected result should be "no updates during wait, no disconnection or exceptions"
