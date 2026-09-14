from flask import Flask, request
import mysql.connector
import os

app = Flask(__name__)


@app.route("/")
def home():
    return "GitOps Platform is running!"


@app.route("/health")
def health():
    return {"status": "healthy"}


@app.route("/db-health")
def db_health():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "mysql"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
        )

        connection.close()

        return {"database": "connected"}

    except Exception as e:
        return {"database": "not connected", "error": str(e)}, 500


@app.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.get_json()

        name = data["name"]
        email = data["email"]

        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "mysql"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
        )

        cursor = connection.cursor()

        query = "INSERT INTO users (name, email) VALUES (%s, %s)"
        cursor.execute(query, (name, email))

        connection.commit()

        user_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return {
            "message": "User created",
            "id": user_id,
            "name": name,
            "email": email
        }, 201

    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/users", methods=["GET"])
def get_users():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "mysql"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
        )

        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users")

        users = cursor.fetchall()

        cursor.close()
        connection.close()

        return {"users": users}

    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)