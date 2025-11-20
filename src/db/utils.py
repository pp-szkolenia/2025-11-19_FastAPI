import os
from dotenv import load_dotenv


def get_db_credentials():
    load_dotenv()
    return {
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "dbname": os.getenv("DB_NAME"),
    }


def get_connection_string():
    credentials = get_db_credentials()
    user = credentials["user"]
    password = credentials["password"]
    host = credentials["host"]
    port = credentials["port"]
    dbname = credentials["dbname"]

    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{dbname}"

