import psycopg2
import os
from .logger import setup_logger


logger = setup_logger("database")


def db_connection() -> psycopg2.extensions.connection:
    try:
        logger.info("Connecting with the db ...")

        conn = psycopg2.connect(
            dbname=os.getenv("dbname", "postgres"),
            user=os.getenv("user", "postgres"),
            password=os.getenv("password", "1234"),
            host=os.getenv("host", "127.0.0.1"),
            port=os.getenv("port", "5432")
        )
        logger.info("Successful connection!")
        return conn
    except Exception as e:
        logger.error(f"Error connecting with the DB: {e}")
        raise e
