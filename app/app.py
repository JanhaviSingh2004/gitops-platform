from flask import Flask
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)