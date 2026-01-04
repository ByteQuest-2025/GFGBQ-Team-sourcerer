from utils.db import fetch_one
from utils.json_utils import make_json_safe


def get_product_by_id(product_id: str) -> dict | None:
    sql = """
    SELECT
        product_id,
        product_name,
        product_type,
        price,
        warranty_days,
        is_refundable,
        high_value,
        created_at,
        updated_at
    FROM products
    WHERE product_id = %s
    """

    row = fetch_one(sql, (product_id,))
    return make_json_safe(row) if row else None
