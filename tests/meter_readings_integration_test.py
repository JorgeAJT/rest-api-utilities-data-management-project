from fastapi.testclient import TestClient
from main import app
from pytest import fixture
import os
from src.utils import db_connection


@fixture
def environmental_variables():
    os.environ["dbname"] = "testing_db"
    os.environ["user"] = "postgres"
    os.environ["password"] = "1234"
    os.environ["host"] = "127.0.0.1"
    os.environ["port"] = "5433"

    return True


@fixture
def test_client():
    return TestClient(app, "http://127.0.0.1:8080")


def test_get_meter_readings_path_params_positive(environmental_variables: bool, test_client: TestClient):
    expected_row = {
        "meter_number": "55933",
        "connection_ean_code": "871694840008583575",
        "account_id": "0100000025",
        "brand": "ESSENT",
        "energy_type": "ELECTRICITY",
        "reading_date": "2023-11-01",
        "reading_electricity": "{\"supplyLow\": 8252.261, \"supplyHigh\": 12784.845, "
                               "\"returnLow\": 0.0, \"returnHigh\": 0.0}",
        "reading_gas": None,
        "rejection": None,
        "validation_status": "VALID"
    }

    meter_readings_id = None

    try:
        with db_connection() as connection:
            with connection.cursor() as cursor:
                values_tuple = tuple(expected_row.values())
                cursor.execute(
                    "INSERT INTO meter_readings "
                    "(meter_number, connection_ean_code, account_id, brand, energy_type, "
                    "reading_date, reading_electricity, reading_gas, rejection, validation_status) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING meter_readings_id",
                    values_tuple
                )
                meter_readings_id = cursor.fetchone()[0]
                connection.commit()

        connection_ean_code = expected_row["connection_ean_code"]
        response = test_client.get(f"/meter_readings/{connection_ean_code}")
        response_json = response.json()

        expected_response = {
            "meter_readings": [
                {
                    "meter_readings_id": meter_readings_id,
                    **expected_row
                }
            ]
        }

        assert response_json["status_code"] == 200
        assert response_json is not None
        assert response_json["message"] == expected_response

        returned_row = response_json["message"]["meter_readings"][0]
        assert returned_row["meter_number"].isdigit(), "meter_number must contain only digits"
        assert returned_row["connection_ean_code"].isdigit(), "connection_ean_code must contain only digits"
        assert returned_row["account_id"].isdigit(), "account_id must contain only digits"

    finally:
        if meter_readings_id is not None:
            with db_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM meter_readings WHERE meter_readings_id = %s", (meter_readings_id,))
                    connection.commit()


def test_get_meter_readings_path_params_negative(environmental_variables: bool, test_client: TestClient):
    non_existent_code = "0000000000000000"
    response = test_client.get(f"/meter_readings/{non_existent_code}")
    response_json = response.json()
    assert response_json["status_code"] == 404
    assert "not found" in response_json["message"]


def test_get_meter_readings_query_params_positive(environmental_variables: bool, test_client: TestClient):
    expected_row = {
        "meter_number": "55933",
        "connection_ean_code": "871694840008583575",
        "account_id": "0100000025",
        "brand": "ESSENT",
        "energy_type": "ELECTRICITY",
        "reading_date": "2023-11-01",
        "reading_electricity": "{\"supplyLow\": 8252.261, \"supplyHigh\": 12784.845, "
                               "\"returnLow\": 0.0, \"returnHigh\": 0.0}",
        "reading_gas": None,
        "rejection": None,
        "validation_status": "VALID"
    }

    meter_readings_id = None

    try:
        with db_connection() as connection:
            with connection.cursor() as cursor:
                values_tuple = tuple(expected_row.values())
                cursor.execute(
                    "INSERT INTO meter_readings "
                    "(meter_number, connection_ean_code, account_id, brand, energy_type, "
                    "reading_date, reading_electricity, reading_gas, rejection, validation_status) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING meter_readings_id",
                    values_tuple
                )
                meter_readings_id = cursor.fetchone()[0]
                connection.commit()

        connection_ean_code = expected_row["connection_ean_code"]
        account_id = expected_row["account_id"]
        response = test_client.get("/meter_readings/", params={
            "account_id": account_id,
            "connection_ean_code": connection_ean_code
        })
        response_json = response.json()

        expected_response = {
            "meter_readings": [
                {
                    "meter_readings_id": meter_readings_id,
                    **expected_row
                }
            ]
        }

        assert response_json["status_code"] == 200
        assert response_json is not None
        assert response_json["message"] == expected_response

        returned_row = response_json["message"]["meter_readings"][0]
        assert returned_row["meter_number"].isdigit(), "meter_number must contain only digits"
        assert returned_row["connection_ean_code"].isdigit(), "connection_ean_code must contain only digits"
        assert returned_row["account_id"].isdigit(), "account_id must contain only digits"

    finally:
        if meter_readings_id is not None:
            with db_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM meter_readings WHERE meter_readings_id = %s", (meter_readings_id,))
                    connection.commit()

"""
def test_post_meter_readings(environmental_variables: bool, test_client: TestClient):
    request_data = {
        "meter_number": "348249",
        "connection_ean_code": "3792862732893473989",
        "account_id": "000000007",
        "brand": "ESSENT",
        "energy_type": "ELECTRICITY",
        "reading_date": "2023-11-01",
        "reading_electricity": "{\"supplyLow\": 8252.261, \"supplyHigh\": 12784.845, "
                               "\"returnLow\": 0.0, \"returnHigh\": 0.0}",
        "reading_gas": None,
        "rejection": None,
        "validation_status": "VALID"
    }
    response = test_client.post("/meter_readings/", json=request_data)
    response_json = response.json()
    assert response_json["status_code"] == 201
    assert response_json is not None
    assert response_json["message"]["meter_readings"]["account_id"] == request_data["account_id"]


def test_put_meter_readings(environmental_variables: bool, test_client: TestClient):
    request_data = {
        "meter_number": "3401345208",
        "connection_ean_code": "871694840015049002",
        "account_id": "000000004",
        "brand": "ESSENT",
        "energy_type": "GAS",
        "reading_date": "2023-11-01",
        "reading_electricity": None,
        "reading_gas": "{\"gasTotal\": 11029.055}",
        "rejection": None,
        "validation_status": "VALID"
    }
    meter_readings_id = 5
    response = test_client.put(f"/meter_readings/{meter_readings_id}", json=request_data)

    expected_response = {
        "meter_readings": {
            "meter_readings_id": meter_readings_id,
            **request_data
        }
    }

    assert response.status_code == 200
    assert response.json() is not None
    assert response.json()["message"] == expected_response

"""
#def test_delete_meter_readings(environmental_variables: bool, test_client: TestClient):

# hacer TODOS los posibles casos y combinaciones incluidos los negativos usando DIRECTAMENTE la base de datos
