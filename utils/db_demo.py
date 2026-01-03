"""
Demo script: connect to Supabase Postgres, fetch data, and run parameterized inserts.

RUN USING:
    python -m utils.db_demo
"""

from utils.db import get_conn, fetch_all, execute


def demo():
    print("🔌 Connecting to Supabase Postgres...")

    conn = get_conn()
    print("✅ Connected to database.")

    # --------------------------------------------------
    # FETCH USERS
    # --------------------------------------------------
    users = fetch_all(
        conn,
        "SELECT user_id, full_name, email FROM users LIMIT 10"
    )

    print("\n📦 Existing users:")
    for u in users:
        print(u)

    # --------------------------------------------------
    # INSERT SAMPLE USER
    # --------------------------------------------------
    sample_user = {
        "user_id": "u_demo_1",
        "full_name": "Demo User",
        "email": "demo@example.com",
        "phone": "+10000000000",
        "loyalty_level": "bronze",
        "rating": 4.2,
        "total_orders": 1,
        "refund_requests": 0,
        "last_refund_date": None,
        "risk_score": 0.1,
        "is_blocked": False,
    }

    insert_user_sql = """
        INSERT INTO users (
            user_id, full_name, email, phone, loyalty_level,
            rating, total_orders, refund_requests, last_refund_date,
            risk_score, is_blocked
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (user_id) DO NOTHING
    """

    execute(
        conn,
        insert_user_sql,
        (
            sample_user["user_id"],
            sample_user["full_name"],
            sample_user["email"],
            sample_user["phone"],
            sample_user["loyalty_level"],
            sample_user["rating"],
            sample_user["total_orders"],
            sample_user["refund_requests"],
            sample_user["last_refund_date"],
            sample_user["risk_score"],
            sample_user["is_blocked"],
        )
    )

    print("✅ Inserted sample user (or skipped if exists).")

    # --------------------------------------------------
    # INSERT SAMPLE PRODUCT
    # --------------------------------------------------
    sample_product = {
        "product_id": "p_demo_1",
        "product_name": "Demo Iron Box",
        "category": "home_appliance",
        "product_type": "iron",
        "price": 2499,
        "warranty_days": 365,
        "is_refundable": True,
        "high_value": False,
    }

    insert_product_sql = """
        INSERT INTO products (
            product_id, product_name, category, product_type,
            price, warranty_days, is_refundable, high_value
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (product_id) DO NOTHING
    """

    execute(
        conn,
        insert_product_sql,
        (
            sample_product["product_id"],
            sample_product["product_name"],
            sample_product["category"],
            sample_product["product_type"],
            sample_product["price"],
            sample_product["warranty_days"],
            sample_product["is_refundable"],
            sample_product["high_value"],
        )
    )

    print("✅ Inserted sample product (or skipped if exists).")

    conn.close()
    print("🔒 Connection closed.")


if __name__ == "__main__":
    demo()
