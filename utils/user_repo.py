from utils.db import fetch_one
from utils.json_utils import make_json_safe


def get_user_by_id(user_id: str) -> dict | None:
    sql = """
    SELECT
        user_id,
        loyalty_level,
        rating,
        total_orders,
        refund_requests
    FROM users
    WHERE user_id = %s
    """

    row = fetch_one(sql, (user_id,))
    return make_json_safe(row) if row else None
