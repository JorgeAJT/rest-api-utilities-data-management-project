from fastapi.testclient import TestClient
from main import app
from tests.utils import (insert_test_data_into_mandate_data,
                         delete_all_test_data, delete_test_data_by_id,
                         get_test_data)
from tests.data import MANDATE_DATA_SINGLE


test_client = TestClient(app, "127.0.0.1:8080")


def test_get_mandate_data_path_params(environmental_variables: bool):
    try:
        expected_row = MANDATE_DATA_SINGLE
        insert_test_data_into_mandate_data(expected_row)

        mandate_id = expected_row["mandate_id"]
        business_partner_id = expected_row["business_partner_id"]
        response = test_client.get(f"/mandate_data/{business_partner_id}")
        response_json = response.json()

        assert response_json["status_code"] == 200
        assert response_json is not None
        assert response_json["message"] == {"mandate_data": [expected_row]}

        returned_row = response_json["message"]["mandate_data"][0]
        assert isinstance(returned_row["mandate_id"], int), "mandate_id must be an integer"
        assert returned_row["business_partner_id"].isdigit(), "business_partner_id must contain only digits"

        delete_test_data_by_id("mandate_data",
                               "mandate_id",
                               mandate_id)

        response = test_client.get(f"/mandate_data/{business_partner_id}")
        response_json = response.json()
        assert response_json["status_code"] == 404
        assert "not found" in response_json["message"]

    finally:
        delete_all_test_data("mandate_data")


def test_get_mandate_data_query_params(environmental_variables: bool):
    try:
        expected_row = MANDATE_DATA_SINGLE
        insert_test_data_into_mandate_data(expected_row)

        mandate_id = expected_row["mandate_id"]
        business_partner_id = expected_row["business_partner_id"]
        mandate_status = expected_row["mandate_status"]
        collection_frequency = expected_row["collection_frequency"]
        response = test_client.get("/mandate_data/", params={
            "business_partner_id": business_partner_id,
            "mandate_status": mandate_status,
            "collection_frequency": collection_frequency
        })
        response_json = response.json()

        assert response_json["status_code"] == 200
        assert response_json is not None
        assert response_json["message"] == {"mandate_data": [expected_row]}

        returned_row = response_json["message"]["mandate_data"][0]
        assert isinstance(returned_row["mandate_id"], int), "mandate_id must be an integer"
        assert returned_row["business_partner_id"].isdigit(), "business_partner_id must contain only digits"

        delete_test_data_by_id("mandate_data",
                               "mandate_id",
                               mandate_id)

        response = test_client.get("/mandate_data/", params={
            "business_partner_id": business_partner_id,
            "mandate_status": mandate_status,
            "collection_frequency": collection_frequency
        })
        response_json = response.json()
        assert response_json["status_code"] == 404
        assert "not found" in response_json["message"]

    finally:
        delete_all_test_data("mandate_data")


def test_post_mandate_data(environmental_variables: bool):
    try:
        request_data = MANDATE_DATA_SINGLE
        response = test_client.post("/mandate_data/", json=request_data)
        response_json = response.json()
        assert response_json["status_code"] == 201
        assert response_json is not None
        assert response_json["message"] == {"mandate_data": [request_data]}

        returned_row = response_json["message"]["mandate_data"][0]
        assert isinstance(returned_row["mandate_id"], int), "mandate_id must be an integer"
        assert returned_row["business_partner_id"].isdigit(), "business_partner_id must contain only digits"

        inserted_row = get_test_data("mandate_data", "business_partner_id",
                                     request_data["business_partner_id"])

        assert returned_row == inserted_row

    finally:
        delete_all_test_data("mandate_data")


def test_put_mandate_data(environmental_variables: bool):
    try:
        request_data = MANDATE_DATA_SINGLE
        insert_test_data_into_mandate_data(request_data)

        mandate_id = request_data["mandate_id"]
        response = test_client.put(f"/mandate_data/{mandate_id}", json=request_data)
        response_json = response.json()

        assert response_json["status_code"] == 201
        assert response_json is not None
        assert response_json["message"] == {"mandate_data": [request_data]}

        returned_row = response_json["message"]["mandate_data"][0]
        assert isinstance(returned_row["mandate_id"], int), "mandate_id must be an integer"
        assert returned_row["business_partner_id"].isdigit(), "business_partner_id must contain only digits"

        delete_test_data_by_id("mandate_data",
                               "mandate_id",
                               mandate_id)

        response = test_client.put(f"/mandate_data/{mandate_id}", json=request_data)
        response_json = response.json()
        assert response_json["status_code"] == 404
        assert "not found" in response_json["message"]

    finally:
        delete_all_test_data("mandate_data")


def test_delete_mandate_data(environmental_variables: bool):
    try:
        data_to_insert = MANDATE_DATA_SINGLE
        insert_test_data_into_mandate_data(data_to_insert)

        mandate_id = data_to_insert["mandate_id"]
        response = test_client.delete(f"/mandate_data/{mandate_id}")
        response_json = response.json()
        assert response_json["status_code"] == 200
        assert response_json is not None
        assert "deleted successfully" in response_json["message"]

        response = test_client.delete(f"/mandate_data/{mandate_id}")
        response_json = response.json()
        assert response_json["status_code"] == 404
        assert "not found" in response_json["message"]

    finally:
        delete_all_test_data("mandate_data")
