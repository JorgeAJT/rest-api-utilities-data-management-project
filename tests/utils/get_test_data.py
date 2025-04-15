from psycopg2.extras import RealDictCursor
from fastapi.encoders import jsonable_encoder
from src.utils import db_connection


def get_test_data(table_name: str, column_name: str, column_value) -> dict:
    with db_connection() as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(f'SELECT * FROM {table_name} WHERE {column_name} = %s', (column_value,))
            row = cursor.fetchone()
            encoded_row = jsonable_encoder(dict(row))
            return encoded_row
