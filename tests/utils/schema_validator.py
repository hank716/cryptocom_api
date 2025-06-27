candlestick_schema = {
    "type": "object",
    "properties": {
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "o": {"type": "string"},
                    "h": {"type": "string"},
                    "l": {"type": "string"},
                    "c": {"type": "string"},
                    "v": {"type": "string"},
                    "t": {"type": "integer"}
                },
                "required": ["o", "h", "l", "c", "v", "t"]
            }
        }
    },
    "required": ["data"]
}
