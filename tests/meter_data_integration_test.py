from fastapi.testclient import TestClient
from main import app
from tests.utils import (insert_test_data_into_meter_data,
                         delete_all_test_data, delete_test_data_by_id,
                         get_test_data)
from tests.data import METER_DATA_SINGLE


test_client = TestClient(app, "127.0.0.1:8080")


def test_get_meter_data_path_params(environmental_variables: bool):
    try:
        expected_row = METER_DATA_SINGLE
        meter_data_id = insert_test_data_into_meter_data(expected_row)

        connection_ean_code = expected_row["connection_ean_code"]
        response = test_client.get(f"/meter_data/{connection_ean_code}")
        response_json = response.json()

        expected_response = {
            "meter_data": [
                {
                    "meter_data_id": meter_data_id,
                    **expected_row
                }
            ]
        }

        assert response_json["status_code"] == 200
        assert response_json is not None
        assert response_json["message"] == expected_response

        returned_row = response_json["message"]["meter_data"][0]
        assert returned_row["meter_number"].isdigit(), "meter_number must contain only digits"
        assert returned_row["connection_ean_code"].isdigit(), "connection_ean_code must contain only digits"
        assert returned_row["business_partner_id"].isdigit(), "business_partner_id must contain only digits"
        assert returned_row["grid_company_code"].isdigit(), "grid_company_code must contain only digits"
        assert returned_row["oda_code"].isdigit(), "oda_code must contain only digits"
        assert returned_row["installation"].isdigit(), "installation must contain only digits"

        delete_test_data_by_id("meter_data",
                               "meter_data_id",
                               meter_data_id)

        response = test_client.get(f"/meter_data/{connection_ean_code}")
        response_json = response.json()
        assert response_json["status_code"] == 404
        assert "not found" in response_json["message"]

    finally:
        delete_all_test_data("meter_data")


def test_get_meter_data_query_params(environmental_variables: bool):
    try:
        expected_row = METER_DATA_SINGLE
        meter_data_id = insert_test_data_into_meter_data(expected_row)

        business_partner_id = expected_row["business_partner_id"]
        connection_ean_code = expected_row["connection_ean_code"]
        response = test_client.get("/meter_data/", params={
            "business_partner_id": business_partner_id,
            "connection_ean_code": connection_ean_code
        })
        response_json = response.json()

        expected_response = {
            "meter_data": [
                {
                    "meter_data_id": meter_data_id,
                    **expected_row
                }
            ]
        }

        assert response_json["status_code"] == 200
        assert response_json is not None
        assert response_json["message"] == expected_response

        returned_row = response_json["message"]["meter_data"][0]
        assert returned_row["meter_number"].isdigit(), "meter_number must contain only digits"
        assert returned_row["connection_ean_code"].isdigit(), "connection_ean_code must contain only digits"
        assert returned_row["business_partner_id"].isdigit(), "business_partner_id must contain only digits"
        assert returned_row["grid_company_code"].isdigit(), "grid_company_code must contain only digits"
        assert returned_row["oda_code"].isdigit(), "oda_code must contain only digits"
        assert returned_row["installation"].isdigit(), "installation must contain only digits"

        delete_test_data_by_id("meter_data",
                               "meter_data_id",
                               meter_data_id)

        response = test_client.get("/meter_data/", params={
            "business_partner_id": business_partner_id,
            "connection_ean_code": connection_ean_code
        })
        response_json = response.json()
        assert response_json["status_code"] == 404
        assert "not found" in response_json["message"]

    finally:
        delete_all_test_data("meter_data")


def test_post_meter_data(environmental_variables: bool):
    try:
        request_data = METER_DATA_SINGLE
        response = test_client.post("/meter_data/", json=request_data)
        response_json = response.json()
        assert response_json["status_code"] == 201
        assert response_json is not None

        returned_row = response_json["message"]["meter_data"][0]
        assert returned_row["meter_number"] == request_data["meter_number"]
        assert returned_row["connection_ean_code"] == request_data["connection_ean_code"]
        assert returned_row["business_partner_id"] == request_data["business_partner_id"]
        assert returned_row["grid_company_code"] == request_data["grid_company_code"]
        assert returned_row["oda_code"] == request_data["oda_code"]
        assert returned_row["installation"] == request_data["installation"]

        assert returned_row["meter_number"].isdigit(), "meter_number must contain only digits"
        assert returned_row["connection_ean_code"].isdigit(), "connection_ean_code must contain only digits"
        assert returned_row["business_partner_id"].isdigit(), "business_partner_id must contain only digits"
        assert returned_row["grid_company_code"].isdigit(), "grid_company_code must contain only digits"
        assert returned_row["oda_code"].isdigit(), "oda_code must contain only digits"
        assert returned_row["installation"].isdigit(), "installation must contain only digits"

        inserted_row = get_test_data("meter_data", "connection_ean_code",
                                     request_data["connection_ean_code"])

        assert returned_row == inserted_row

    finally:
        delete_all_test_data("meter_data")


def test_put_meter_data(environmental_variables: bool):
    try:
        request_data = METER_DATA_SINGLE
        meter_data_id = insert_test_data_into_meter_data(request_data)
        response = test_client.put(f"/meter_data/{meter_data_id}", json=request_data)
        response_json = response.json()

        expected_response = {
            "meter_data": [
                {
                    "meter_data_id": meter_data_id,
                    **request_data
                }
            ]
        }

        assert response_json["status_code"] == 201
        assert response_json is not None
        assert response_json["message"] == expected_response

        returned_row = response_json["message"]["meter_data"][0]
        assert returned_row["meter_number"].isdigit(), "meter_number must contain only digits"
        assert returned_row["connection_ean_code"].isdigit(), "connection_ean_code must contain only digits"
        assert returned_row["business_partner_id"].isdigit(), "business_partner_id must contain only digits"
        assert returned_row["grid_company_code"].isdigit(), "grid_company_code must contain only digits"
        assert returned_row["oda_code"].isdigit(), "oda_code must contain only digits"
        assert returned_row["installation"].isdigit(), "installation must contain only digits"

        delete_test_data_by_id("meter_data",
                               "meter_data_id",
                               meter_data_id)

        response = test_client.put(f"/meter_data/{meter_data_id}", json=request_data)
        response_json = response.json()
        assert response_json["status_code"] == 404
        assert "not found" in response_json["message"]

    finally:
        delete_all_test_data("meter_data")


def test_delete_meter_data(environmental_variables: bool):
    try:
        data_to_insert = METER_DATA_SINGLE
        meter_data_id = insert_test_data_into_meter_data(data_to_insert)
        response = test_client.delete(f"/meter_data/{meter_data_id}")
        response_json = response.json()
        assert response_json["status_code"] == 200
        assert response_json is not None
        assert "deleted successfully" in response_json["message"]

        response = test_client.delete(f"/meter_data/{meter_data_id}")
        response_json = response.json()
        assert response_json["status_code"] == 404
        assert "not found" in response_json["message"]

    finally:
        delete_all_test_data("meter_data")
