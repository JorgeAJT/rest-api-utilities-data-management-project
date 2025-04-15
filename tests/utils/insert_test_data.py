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


def insert_test_data_into_meter_data(test_data: dict) -> int:
    with db_connection() as connection:
        with connection.cursor() as cursor:
            values_tuple = tuple(test_data.values())
            cursor.execute(
                "INSERT INTO meter_data "
                "(meter_number, connection_ean_code, business_partner_id, brand, "
                "grid_company_code, oda_code, smart_collectable, sjv1, sjv2, installation, "
                "division, move_out_date, row_create_datetime, move_in_date) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                "RETURNING meter_data_id",
                values_tuple)
            meter_data_id = cursor.fetchone()[0]
            connection.commit()

            return meter_data_id


def insert_test_data_into_mandate_data(test_data: dict) -> bool:
    with db_connection() as connection:
        with connection.cursor() as cursor:
            values_tuple = tuple(test_data.values())
            cursor.execute(
                "INSERT INTO mandate_data "
                "(mandate_id, business_partner_id, brand, "
                "mandate_status, collection_frequency, row_update_datetime, "
                "row_create_datetime, changed_by, collection_type, metering_consent) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                values_tuple)
            connection.commit()

            return True
