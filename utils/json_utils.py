from decimal import Decimal
from datetime import datetime, date


def make_json_safe(data):
    """
    Recursively convert non-JSON-serializable objects
    (Decimal, datetime, date) into safe formats.
    """
    if isinstance(data, dict):
        return {k: make_json_safe(v) for k, v in data.items()}

    if isinstance(data, list):
        return [make_json_safe(v) for v in data]

    if isinstance(data, Decimal):
        return int(data) if data % 1 == 0 else float(data)

    if isinstance(data, (datetime, date)):
        return data.isoformat()

    return data
