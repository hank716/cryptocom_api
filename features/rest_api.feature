Feature: REST API: public/get-candlestick

  Scenario: TC1 - Valid request returns candlestick data
    Given REST test input "instrument_name=BTC_USDT, timeframe=5m"
    Then REST expected result should be "TC1 - HTTP 200 and code == 0, result.data contains multiple entries"

  Scenario: TC2 - Test various timeframe formats
    Given REST test input "instrument_name=BTC_USDT, timeframe=1m"
    Then REST expected result should be "TC2 - HTTP 200 and timestamps reflect 1-minute intervals"

  Scenario: TC3 - Validate candlestick fields and structure
    Given REST test input "any valid request"
    Then REST expected result should be "TC3 - Each candlestick contains timestamp, open, high, low, close, volume"

  Scenario: TC4 - Maximum data limit test
    Given REST test input "instrument_name=BTC_USDT, timeframe=1m, limit=5000"
    Then REST expected result should be "TC4 - Result contains at most 5000 entries, HTTP 200 and stable response"

  Scenario: TC5 - Missing required parameter
    Given REST test input "missing instrument_name"
    Then REST expected result should be "TC5 - code != 0 due to missing instrument_name"

  Scenario: TC6 - Specific time range query
    Given REST test input "instrument_name=BTC_USDT, timeframe=5m, start=NOW_MINUS_1H, end=NOW"
    Then REST expected result should be "TC6 - All timestamps are within the specified range"

  Scenario: TC7 - Invalid instrument name
    Given REST test input "instrument_name=INVALID_COIN"
    Then REST expected result should be "TC7 - code != 0 due to invalid instrument_name"

  Scenario: TC8 - Invalid timeframe format
    Given REST test input "timeframe=abc"
    Then REST expected result should be "TC8 - code != 0 due to invalid timeframe"

  Scenario: TC9 - No parameters provided
    Given REST test input "empty body or query"
    Then REST expected result should be "TC9 - code != 0 due to missing parameters"