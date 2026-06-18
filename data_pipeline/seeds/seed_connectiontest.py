import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="ecommerce_db",
    user="ecommerce_user",
    password="ecommerce_password",
    port=5432
)

print("Connected successfully")

conn.close()