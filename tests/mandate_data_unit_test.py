import pytest
from src.mandate_data import (
    get_mandate_data_by_path_params,
    get_mandate_data_by_query_params,
    post_mandate_data, put_mandate_data,
    delete_mandate_data)
from src.models import MandateData
from tests.fixtures import db_cursor_mock
from tests.data import MANDATE_DATA_LIST, MANDATE_DATA_SINGLE


@pytest.mark.asyncio
async def test_get_mandate_data_by_path_params(mocker, db_cursor_mock):
    expected_rows = MANDATE_DATA_LIST

    mock_db, mock_cursor = db_cursor_mock
    mock_cursor.fetchall.return_value = expected_rows
    mocker.patch("src.mandate_data.get.db_connection", return_value=mock_db)

    business_partner_id = expected_rows[0]["business_partner_id"]
    response = await get_mandate_data_by_path_params(business_partner_id)

    mock_cursor.execute.assert_called_once_with('SELECT * FROM mandate_data WHERE business_partner_id = %s',
                                                (business_partner_id,))

    assert response.model_dump() == {"status_code": 200, "message": {"mandate_data": expected_rows}}


@pytest.mark.asyncio
async def test_get_mandate_data_by_query_params(mocker, db_cursor_mock):
    expected_rows = MANDATE_DATA_LIST

    mock_db, mock_cursor = db_cursor_mock
    mock_cursor.fetchall.return_value = expected_rows
    mocker.patch("src.mandate_data.get.db_connection", return_value=mock_db)

    business_partner_id = expected_rows[0]["business_partner_id"]
    mandate_status = expected_rows[0]["mandate_status"]
    collection_frequency = expected_rows[0]["collection_frequency"]
    response = await get_mandate_data_by_query_params(business_partner_id, mandate_status, collection_frequency)

    mock_cursor.execute.assert_called_once_with("SELECT * FROM mandate_data WHERE business_partner_id = %s "
                                                "AND mandate_status = %s AND collection_frequency = %s",
                                                (business_partner_id, mandate_status, collection_frequency))

    assert response.model_dump() == {"status_code": 200, "message": {"mandate_data": expected_rows}}


@pytest.mark.asyncio
async def test_post_mandate_data(mocker, db_cursor_mock):
    request_data = MANDATE_DATA_SINGLE

    mandate_data_request = MandateData(**request_data)

    mock_db, mock_cursor = db_cursor_mock
    mocker.patch("src.mandate_data.post.db_connection", return_value=mock_db)

    response = await post_mandate_data(mandate_data_request)

    expected_query = ("INSERT INTO mandate_data "
                      "(mandate_id, business_partner_id, brand, "
                      "mandate_status, collection_frequency, row_update_datetime, "
                      "row_create_datetime, changed_by, collection_type, metering_consent) "
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

    expected_params = tuple(mandate_data_request.model_dump().values())

    mock_cursor.execute.assert_called_once_with(expected_query, expected_params)
    mock_db.commit.assert_called_once_with()

    assert response.model_dump() == {"status_code": 201,
                                     "message": {"mandate_data": [mandate_data_request.model_dump()]}}


@pytest.mark.asyncio
async def test_put_mandate_data(mocker, db_cursor_mock):
    request_data = MANDATE_DATA_SINGLE

    mandate_data_request = MandateData(**request_data)

    mock_db, mock_cursor = db_cursor_mock
    mocker.patch("src.mandate_data.put.db_connection", return_value=mock_db)

    mandate_id = request_data["mandate_id"]
    response = await put_mandate_data(mandate_id, mandate_data_request)

    expected_query = ("UPDATE mandate_data "
                      "SET mandate_id = %s, "
                      "business_partner_id = %s, "
                      "brand = %s, mandate_status = %s, "
                      "collection_frequency = %s, "
                      "row_update_datetime = %s, "
                      "row_create_datetime = %s, "
                      "changed_by = %s, "
                      "collection_type = %s, "
                      "metering_consent = %s "
                      "WHERE mandate_id = %s")

    expected_params = tuple(mandate_data_request.model_dump().values()) + (mandate_id,)

    mock_cursor.execute.assert_any_call(expected_query, expected_params)
    mock_db.commit.assert_called_once_with()

    assert response.model_dump() == {"status_code": 201,
                                     "message": {"mandate_data": [mandate_data_request.model_dump()]}}


@pytest.mark.asyncio
async def test_delete_mandate_data(mocker, db_cursor_mock):
    mock_db, mock_cursor = db_cursor_mock
    mocker.patch("src.mandate_data.delete.db_connection", return_value=mock_db)

    mandate_id = MANDATE_DATA_SINGLE["mandate_id"]
    response = await delete_mandate_data(mandate_id)
    response_dict = response.model_dump()

    mock_cursor.execute.assert_any_call('DELETE FROM mandate_data WHERE mandate_id = %s',
                                        (mandate_id,))
    mock_db.commit.assert_called_once_with()

    assert response_dict["status_code"] == 200
    assert "deleted successfully" in response_dict["message"]
