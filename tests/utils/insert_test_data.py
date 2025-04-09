from src.utils import db_connection


def insert_test_data_into_meter_readings(test_data: dict) -> int:
    with db_connection() as connection:
        with connection.cursor() as cursor:
            values_tuple = tuple(test_data.values())
            cursor.execute(
                "INSERT INTO meter_readings "
                "(meter_number, connection_ean_code, account_id, brand, energy_type, "
                "reading_date, reading_electricity, reading_gas, rejection, validation_status) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING meter_readings_id",
                values_tuple)
            meter_readings_id = cursor.fetchone()[0]
            connection.commit()

            return meter_readings_id
