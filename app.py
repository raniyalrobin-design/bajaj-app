from flask import Flask, jsonify, request
import psycopg2
import os
app = Flask(__name__)

# CI PR test

def get_db_connection():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]    
    )


@app.route("/")
def home():
    return "Bajaj Bicycle Store - Application Server v2 is running!"


@app.route("/health")
def health():
    return jsonify({
        "status": "UP",
        "server": "Flask App VM"
    })


@app.route("/products", methods=["GET"])
def get_products():

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, name, price, stock FROM products ORDER BY id"
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    products = []

    for row in rows:
        products.append({
            "id": row[0],
            "name": row[1],
            "price": float(row[2]),
            "stock": row[3]
        })

    return jsonify(products)


@app.route("/login", methods=["GET"])
def login():

    username = request.args.get("username", "")
    password = request.args.get("password", "")

    connection = get_db_connection()
    cursor = connection.cursor()

    # INTENTIONALLY VULNERABLE — FOR OUR LOCAL LAB ONLY
    query = (
        "SELECT id, username FROM demo_users "
        "WHERE username = '" + username +
        "' AND password = '" + password + "'"
    )

    print("HTTP username:", username)
    print("HTTP password:", password)
    print("SQL generated:", query)

    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    if result:
        return jsonify({
            "login": "SUCCESS",
            "users_returned": result
        })

    return jsonify({
        "login": "FAILED"
    }), 401


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
