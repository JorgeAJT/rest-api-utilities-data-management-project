from src.utils import db_connection


def delete_all_test_data(table_name: str) -> bool:
    with db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM {table_name}")
            connection.commit()

            return True


def delete_test_data_by_id(table_name: str, id_column: str, row_id) -> bool:
    with db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM {table_name} WHERE {id_column} = %s", (row_id,))
            connection.commit()

            return True
