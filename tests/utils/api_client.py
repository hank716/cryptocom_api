import requests
import os

class APIClient:
    def __init__(self, base_url=None):
        self.base_url = base_url or os.getenv("BASE_URL")

    def get_candlestick(self, instrument_name, timeframe):
        endpoint = f"{self.base_url}/public/get-candlestick"
        params = {
            "instrument_name": instrument_name,
            "timeframe": timeframe
        }
        response = requests.get(endpoint, params=params)
        return response
