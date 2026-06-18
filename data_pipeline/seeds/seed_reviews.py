import random
import json
import psycopg2

from datetime import datetime, timedelta


conn = psycopg2.connect(
    host="localhost",
    database="ecommerce_db",
    user="ecommerce_user",
    password="ecommerce_password",
    port=5432
)

cursor = conn.cursor()


def random_past_date():
    days_ago = random.randint(1, 90)
    return datetime.now() - timedelta(days=days_ago)


reviews = [
    "Amazing product",
    "Battery life is excellent",
    "Worth the price",
    "Could be better",
    "Performance is top notch",
    "Very satisfied",
    "Display quality is amazing",
    "Not worth the money",
    "Camera quality excellent"
]


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


print("Creating reviews...")

cursor.execute("SELECT id FROM users")
users = [x[0] for x in cursor.fetchall()]

cursor.execute("SELECT id FROM products")
products = [x[0] for x in cursor.fetchall()]


for _ in range(40):

    user_id = random.choice(users)
    product_id = random.choice(products)

    rating = random.choices(
        [5, 4, 3, 2, 1],
        weights=[40, 30, 15, 10, 5]
    )[0]

    cursor.execute(
        """
        INSERT INTO product_reviews
        (
            product_id,
            user_id,
            rating,
            review_text,
            created_at
        )
        VALUES (%s,%s,%s,%s,%s)
        RETURNING id
        """,
        (
            product_id,
            user_id,
            rating,
            random.choice(reviews),
            random_past_date()
        )
    )

    review_id = cursor.fetchone()[0]

    create_event(
        "review_created",
        "review",
        review_id,
        {
            "product_id": product_id,
            "rating": rating
        }
    )


conn.commit()

print("40 Reviews created")
print("Review events created")

cursor.close()
conn.close()