import psycopg2
import os
from .logger import setup_logger


logger = setup_logger("database")


def db_connection() -> psycopg2.extensions.connection:
    try:
        logger.info("Connecting with the db ...")

        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "users-db"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST", "127.0.0.1"),
            port=os.getenv("DB_PORT", "5432")
        )
        logger.info("Successful connection!")
        return conn
    except Exception as e:
        logger.error(f"Error connecting with the DB: {e}")
        raise e
