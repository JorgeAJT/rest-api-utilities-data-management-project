import psycopg2
from .logger import setup_logger

logger = setup_logger("database")

def db_connection() -> psycopg2.extensions.connection:
    try:
        logger.info("Connecting with the db ...")

        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='1234',
        )
        logger.info("Successful connection!")
        return conn
    except Exception as e:
        logger.error(f"Error connecting with the DB: {e}")
        raise e