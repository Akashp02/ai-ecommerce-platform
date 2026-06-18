import random
import json
import uuid
import bcrypt
import psycopg2

from faker import Faker
from datetime import datetime, timedelta


fake = Faker("en_IN")


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


def hash_password():
    password = "Password@123"
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


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
            "seed_data",
            random_past_date()
        )
    )


# ==========================
# CREATE USERS
# ==========================

user_ids = []

print("Creating users...")

for _ in range(30):

    first_name = fake.first_name()
    last_name = fake.last_name()

    email = f"{first_name.lower()}.{uuid.uuid4().hex[:5]}@gmail.com"

    cursor.execute(
        """
        INSERT INTO users
        (first_name,last_name,email,password_hash,is_active,created_at,role)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
        """,
        (
            first_name,
            last_name,
            email,
            hash_password(),
            True,
            random_past_date(),
            "customer"
        )
    )

    user_id = cursor.fetchone()[0]

    user_ids.append(user_id)

    create_event(
        "user_registered",
        "user",
        user_id,
        {
            "email": email
        }
    )

    create_audit(
        user_id,
        "user_registered",
        "user",
        user_id
    )


# ==========================
# CREATE ADDRESSES
# ==========================

cities = [
    "Mumbai",
    "Delhi",
    "Bangalore",
    "Hyderabad",
    "Pune",
    "Kolkata",
    "Chennai",
    "Bhubaneswar"
]

address_ids = []

print("Creating addresses...")

for user_id in user_ids:

    address_count = random.randint(1, 3)

    for i in range(address_count):

        city = random.choice(cities)

        cursor.execute(
            """
            INSERT INTO addresses
            (
                user_id,
                full_name,
                phone_number,
                address_line1,
                address_line2,
                city,
                state,
                country,
                postal_code,
                is_default,
                created_at
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING id
            """,
            (
                user_id,
                fake.name(),
                fake.phone_number()[:15],
                fake.street_address(),
                "",
                city,
                "State",
                "India",
                str(random.randint(100000, 999999)),
                i == 0,
                random_past_date()
            )
        )

        address_id = cursor.fetchone()[0]

        address_ids.append(
            {
                "user_id": user_id,
                "address_id": address_id
            }
        )


# ==========================
# PRODUCTS
# ==========================

mobile_brands = [
    "iPhone",
    "Samsung",
    "Google Pixel",
    "OnePlus",
    "Xiaomi"
]

laptop_brands = [
    "MacBook",
    "Dell XPS",
    "HP Spectre",
    "Lenovo ThinkPad",
    "Asus ROG"
]

print("Creating products...")


for i in range(25):

    brand = random.choice(mobile_brands)

    name = f"{brand} {random.randint(10,20)}"

    sku = f"MOB-{uuid.uuid4().hex[:8].upper()}"

    price = random.randint(15000, 120000)

    cursor.execute(
        """
        INSERT INTO products
        (
            sku,
            name,
            description,
            price,
            stock_quantity,
            is_available,
            created_at,
            category_id,
            is_active
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
        """,
        (
            sku,
            name,
            f"{name} smartphone",
            price,
            random.randint(20, 100),
            True,
            random_past_date(),
            1,
            True
        )
    )

    product_id = cursor.fetchone()[0]

    create_event(
        "product_created",
        "product",
        product_id,
        {
            "category": "mobile",
            "price": price
        }
    )


for i in range(22):

    brand = random.choice(laptop_brands)

    name = f"{brand} {random.randint(1,10)}"

    sku = f"LAP-{uuid.uuid4().hex[:8].upper()}"

    price = random.randint(35000, 250000)

    cursor.execute(
        """
        INSERT INTO products
        (
            sku,
            name,
            description,
            price,
            stock_quantity,
            is_available,
            created_at,
            category_id,
            is_active
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
        """,
        (
            sku,
            name,
            f"{name} laptop",
            price,
            random.randint(10, 80),
            True,
            random_past_date(),
            2,
            True
        )
    )

    product_id = cursor.fetchone()[0]

    create_event(
        "product_created",
        "product",
        product_id,
        {
            "category": "laptop",
            "price": price
        }
    )


conn.commit()

print("Done.")
print("Users created: 30")
print("Addresses created")
print("Products created: 47")
print("Events created")
print("Audit logs created")


cursor.close()
conn.close()