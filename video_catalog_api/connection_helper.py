import psycopg2
from dotenv import load_dotenv
from os.path import join, dirname
import os

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

# Database connection parameters
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def db_connection():
    connection = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )
    return connection
