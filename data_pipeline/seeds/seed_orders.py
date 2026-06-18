import random
import json
import uuid
import psycopg2

from datetime import datetime, timedelta


# ==========================
# DB CONNECTION
# ==========================

conn = psycopg2.connect(
    host="localhost",
    database="ecommerce_db",
    user="ecommerce_user",
    password="ecommerce_password",
    port=5432
)

cursor = conn.cursor()


# ==========================
# HELPERS
# ==========================

def random_past_date():
    days_ago = random.randint(1, 90)
    return datetime.now() - timedelta(days=days_ago)


def create_event(event_type, entity_type, entity_id, payload):

    cursor.execute(
        """
        INSERT INTO events
        (event_type, entity_type, entity_id, payload, created_at)
        VALUES (%s,%s,%s,%s,%s)
        """,
        (
            event_type,
            entity_type,
            entity_id,
            json.dumps(payload),
            random_past_date()
        )
    )


def create_audit(user_id, action, entity_type, entity_id):

    cursor.execute(
        """
        INSERT INTO audit_logs
        (user_id, action, entity_type, entity_id, metadata, created_at)
        VALUES (%s,%s,%s,%s,%s,%s)
        """,
        (
            user_id,
            action,
            entity_type,
            entity_id,
            "seed_order_data",
            random_past_date()
        )
    )


# ==========================
# FETCH EXISTING DATA
# ==========================

cursor.execute("SELECT id FROM users WHERE role='customer'")
users = [x[0] for x in cursor.fetchall()]

cursor.execute("SELECT id,user_id FROM addresses")
addresses = cursor.fetchall()

cursor.execute(
    """
    SELECT id, price, stock_quantity
    FROM products
    WHERE is_active = true
    """
)
products = cursor.fetchall()


# ==========================
# STATUS DISTRIBUTION
# ==========================

order_statuses = [
    "delivered",
    "delivered",
    "delivered",
    "shipped",
    "processing",
    "confirmed",
    "cancelled"
]

payment_statuses = [
    "paid",
    "paid",
    "paid",
    "paid",
    "failed",
    "pending"
]

payment_methods = [
    "upi",
    "credit_card",
    "debit_card",
    "net_banking"
]


# ==========================
# CREATE ORDERS
# ==========================

print("Creating orders...")

for _ in range(120):

    user_id = random.choice(users)

    user_addresses = [
        a for a in addresses
        if a[1] == user_id
    ]

    if not user_addresses:
        continue

    address_id = random.choice(user_addresses)[0]

    selected_products = random.sample(
        products,
        random.randint(1, 4)
    )

    total_amount = 0
    order_items = []

    for product in selected_products:

        product_id = product[0]
        price = product[1]
        stock = product[2]

        if stock <= 2:
            continue

        quantity = random.randint(1, 2)

        subtotal = price * quantity

        total_amount += subtotal

        order_items.append({
            "product_id": product_id,
            "quantity": quantity,
            "price": price,
            "subtotal": subtotal
        })

        # deduct stock

        cursor.execute(
            """
            UPDATE products
            SET stock_quantity = stock_quantity - %s
            WHERE id = %s
            """,
            (quantity, product_id)
        )

    if len(order_items) == 0:
        continue

    order_status = random.choice(order_statuses)
    payment_status = random.choice(payment_statuses)

    # create order

    cursor.execute(
        """
        INSERT INTO orders
        (
            user_id,
            address_id,
            total_amount,
            order_status,
            payment_status,
            created_at
        )
        VALUES (%s,%s,%s,%s,%s,%s)
        RETURNING id
        """,
        (
            user_id,
            address_id,
            total_amount,
            order_status,
            payment_status,
            random_past_date()
        )
    )

    order_id = cursor.fetchone()[0]

    # create order items

    for item in order_items:

        cursor.execute(
            """
            INSERT INTO order_items
            (
                order_id,
                product_id,
                quantity,
                price_at_purchase,
                subtotal
            )
            VALUES (%s,%s,%s,%s,%s)
            """,
            (
                order_id,
                item["product_id"],
                item["quantity"],
                item["price"],
                item["subtotal"]
            )
        )

    # payment

    cursor.execute(
        """
        INSERT INTO payments
        (
            order_id,
            amount,
            payment_method,
            payment_status,
            transaction_id,
            created_at
        )
        VALUES (%s,%s,%s,%s,%s,%s)
        """,
        (
            order_id,
            total_amount,
            random.choice(payment_methods),
            payment_status,
            str(uuid.uuid4()),
            random_past_date()
        )
    )

    # events

    create_event(
        "order_created",
        "order",
        order_id,
        {
            "user_id": user_id,
            "amount": total_amount,
            "product_count": len(order_items)
        }
    )

    create_event(
        f"payment_{payment_status}",
        "payment",
        order_id,
        {
            "order_id": order_id,
            "amount": total_amount
        }
    )

    # audit

    create_audit(
        user_id,
        "order_created",
        "order",
        order_id
    )


conn.commit()

print("120 Orders created")
print("Payments created")
print("Order items created")
print("Events created")

cursor.close()
conn.close()