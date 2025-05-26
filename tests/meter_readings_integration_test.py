from fastapi.testclient import TestClient
from main import app
from tests.utils import (insert_test_data_into_meter_readings,
                         delete_all_test_data, delete_test_data_by_id,
                         get_test_data)
from tests.data import METER_READINGS_SINGLE


test_client = TestClient(app, "127.0.0.1:8080")


def test_get_meter_readings_path_params(environmental_variables: bool):
    try:
        expected_row = METER_READINGS_SINGLE
        meter_readings_id = insert_test_data_into_meter_readings(expected_row)

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

        delete_test_data_by_id("meter_readings",
                               "meter_readings_id",
                               meter_readings_id)

        response = test_client.get(f"/meter_readings/{connection_ean_code}")
        response_json = response.json()
        assert response_json["status_code"] == 404
        assert "not found" in response_json["message"]

    finally:
        delete_all_test_data("meter_readings")


def test_get_meter_readings_query_params(environmental_variables: bool):
    try:
        expected_row = METER_READINGS_SINGLE
        meter_readings_id = insert_test_data_into_meter_readings(expected_row)

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

        delete_test_data_by_id("meter_readings",
                               "meter_readings_id",
                               meter_readings_id)

        response = test_client.get("/meter_readings/", params={
            "account_id": account_id,
            "connection_ean_code": connection_ean_code
        })
        response_json = response.json()
        assert response_json["status_code"] == 404
        assert "not found" in response_json["message"]

    finally:
        delete_all_test_data("meter_readings")


def test_post_meter_readings(environmental_variables: bool):
    try:
        request_data = METER_READINGS_SINGLE
        response = test_client.post("/meter_readings/", json=request_data)
        response_json = response.json()
        assert response_json["status_code"] == 201
        assert response_json is not None

        returned_row = response_json["message"]["meter_readings"][0]
        assert returned_row["meter_number"] == request_data["meter_number"]
        assert returned_row["connection_ean_code"] == request_data["connection_ean_code"]
        assert returned_row["account_id"] == request_data["account_id"]

        assert returned_row["meter_number"].isdigit(), "meter_number must contain only digits"
        assert returned_row["connection_ean_code"].isdigit(), "connection_ean_code must contain only digits"
        assert returned_row["account_id"].isdigit(), "account_id must contain only digits"

        inserted_row = get_test_data("meter_readings", "connection_ean_code",
                                     request_data["connection_ean_code"])

        assert returned_row == inserted_row

    finally:
        delete_all_test_data("meter_readings")


def test_put_meter_readings(environmental_variables: bool):
    try:
        request_data = METER_READINGS_SINGLE
        meter_readings_id = insert_test_data_into_meter_readings(request_data)
        response = test_client.put(f"/meter_readings/{meter_readings_id}", json=request_data)
        response_json = response.json()

        expected_response = {
            "meter_readings": [
                {
                    "meter_readings_id": meter_readings_id,
                    **request_data
                }
            ]
        }

        assert response_json["status_code"] == 201
        assert response_json is not None
        assert response_json["message"] == expected_response

        returned_row = response_json["message"]["meter_readings"][0]
        assert returned_row["meter_number"].isdigit(), "meter_number must contain only digits"
        assert returned_row["connection_ean_code"].isdigit(), "connection_ean_code must contain only digits"
        assert returned_row["account_id"].isdigit(), "account_id must contain only digits"

        delete_test_data_by_id("meter_readings",
                               "meter_readings_id",
                               meter_readings_id)

        response = test_client.put(f"/meter_readings/{meter_readings_id}", json=request_data)
        response_json = response.json()
        assert response_json["status_code"] == 404
        assert "not found" in response_json["message"]

    finally:
        delete_all_test_data("meter_readings")


def test_delete_meter_readings(environmental_variables: bool):
    try:
        data_to_insert = METER_READINGS_SINGLE
        meter_readings_id = insert_test_data_into_meter_readings(data_to_insert)
        response = test_client.delete(f"/meter_readings/{meter_readings_id}")
        response_json = response.json()
        assert response_json["status_code"] == 200
        assert response_json is not None
        assert "deleted successfully" in response_json["message"]

        response = test_client.delete(f"/meter_readings/{meter_readings_id}")
        response_json = response.json()
        assert response_json["status_code"] == 404
        assert "not found" in response_json["message"]

    finally:
        delete_all_test_data("meter_readings")
