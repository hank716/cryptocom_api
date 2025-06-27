Feature: REST API: public/get-candlestick

  Scenario: TC1 - Valid request returns candlestick data
    Given REST test input "instrument_name=BTC_USDT, timeframe=5m"
    Then REST expected result should be "HTTP 200, result.data contains multiple entries"

  Scenario: TC2 - Test various timeframe formats
    Given REST test input "instrument_name=BTC_USDT, timeframe=1m"
    Then REST expected result should be "HTTP 200, data matches timeframe granularity"

  Scenario: TC3 - Validate candlestick fields and structure
    Given REST test input "any valid request"
    Then REST expected result should be "Each item contains timestamp, open, high, low, close, volume"

  Scenario: TC4 - Maximum data limit test
    Given REST test input "limit=5000"
    Then REST expected result should be "Response contains maximum allowed entries and system remains stable"

  Scenario: TC5 - Missing required parameter
    Given REST test input "missing instrument_name"
    Then REST expected result should be "HTTP 400 error"

  Scenario: TC6 - Specific time range query
    Given REST test input "start/end range within one hour"
    Then REST expected result should be "Data is within the specified time range"

  Scenario: TC7 - Invalid instrument name
    Given REST test input "instrument_name=INVALID_COIN"
    Then REST expected result should be "HTTP 400 or code != 0"

  Scenario: TC8 - Invalid timeframe format
    Given REST test input "timeframe=abc"
    Then REST expected result should be "HTTP 400 or code != 0"

  Scenario: TC9 - No parameters provided
    Given REST test input "empty body or query"
    Then REST expected result should be "HTTP 400 with message indicating missing parameters"
