import pytest
from src.meter_readings import (
    get_meter_readings_by_path_params,
    get_meter_readings_by_query_params,
    post_meter_readings, put_meter_readings,
    delete_meter_readings)
from src.models import MeterReadingsRequest
from tests.fixtures import db_cursor_mock
from tests.data import METER_READINGS_LIST, METER_READINGS_SINGLE


@pytest.mark.asyncio
async def test_get_meter_readings_by_path_params(mocker, db_cursor_mock):
    expected_rows = METER_READINGS_LIST

    mock_db, mock_cursor = db_cursor_mock
    mock_cursor.fetchall.return_value = expected_rows
    mocker.patch("src.meter_readings.get.db_connection", return_value=mock_db)

    connection_ean_code = expected_rows[0]["connection_ean_code"]
    response = await get_meter_readings_by_path_params(connection_ean_code)

    mock_cursor.execute.assert_called_once_with('SELECT * FROM meter_readings WHERE connection_ean_code = %s',
                                                (connection_ean_code,))

    assert response.model_dump() == {"status_code": 200, "message": {"meter_readings": expected_rows}}


@pytest.mark.asyncio
async def test_get_meter_readings_by_query_params(mocker, db_cursor_mock):
    expected_rows = METER_READINGS_LIST

    mock_db, mock_cursor = db_cursor_mock
    mock_cursor.fetchall.return_value = expected_rows
    mocker.patch("src.meter_readings.get.db_connection", return_value=mock_db)

    account_id = expected_rows[0]["account_id"]
    connection_ean_code = expected_rows[0]["connection_ean_code"]
    response = await get_meter_readings_by_query_params(account_id, connection_ean_code)

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM meter_readings WHERE account_id = %s AND connection_ean_code = %s",
        (account_id, connection_ean_code)
    )

    assert response.model_dump() == {"status_code": 200, "message": {"meter_readings": expected_rows}}


@pytest.mark.asyncio
async def test_post_meter_readings(mocker, db_cursor_mock):
    request_data = METER_READINGS_SINGLE

    meter_readings_request = MeterReadingsRequest(**request_data)

    mock_db, mock_cursor = db_cursor_mock
    mock_cursor.fetchone.return_value = (100,)
    mocker.patch("src.meter_readings.post.db_connection", return_value=mock_db)

    response = await post_meter_readings(meter_readings_request)

    expected_query = ("INSERT INTO meter_readings "
                      "(meter_number, connection_ean_code, account_id, brand, energy_type, "
                      "reading_date, reading_electricity, reading_gas, rejection, validation_status) "
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING meter_readings_id")

    expected_params = tuple(meter_readings_request.model_dump().values())

    mock_cursor.execute.assert_called_once_with(expected_query, expected_params)
    mock_db.commit.assert_called_once_with()

    expected_response = {
        "status_code": 201,
        "message": {
            "meter_readings": [
                {
                    "meter_readings_id": 100,
                    **meter_readings_request.model_dump()
                }
            ]
        }
    }

    assert response.model_dump() == expected_response


@pytest.mark.asyncio
async def test_put_meter_readings(mocker, db_cursor_mock):
    request_data = METER_READINGS_SINGLE

    meter_readings_request = MeterReadingsRequest(**request_data)

    mock_db, mock_cursor = db_cursor_mock
    mocker.patch("src.meter_readings.put.db_connection", return_value=mock_db)

    meter_readings_id = 3
    response = await put_meter_readings(meter_readings_id, meter_readings_request)

    expected_query = ("UPDATE meter_readings "
                      "SET meter_number = %s, "
                      "connection_ean_code = %s, "
                      "account_id = %s, "
                      "brand = %s, "
                      "energy_type = %s,"
                      "reading_date = %s, "
                      "reading_electricity = %s, "
                      "reading_gas = %s, "
                      "rejection = %s, "
                      "validation_status = %s "
                      "WHERE meter_readings_id = %s")

    expected_params = tuple(meter_readings_request.model_dump().values()) + (meter_readings_id,)

    mock_cursor.execute.assert_any_call(expected_query, expected_params)
    mock_db.commit.assert_called_once_with()

    expected_response = {
        "status_code": 201,
        "message": {
            "meter_readings": [
                {
                    "meter_readings_id": meter_readings_id,
                    **meter_readings_request.model_dump()
                }
            ]
        }
    }

    assert response.model_dump() == expected_response


@pytest.mark.asyncio
async def test_delete_meter_readings(mocker, db_cursor_mock):
    mock_db, mock_cursor = db_cursor_mock
    mocker.patch("src.meter_readings.delete.db_connection", return_value=mock_db)

    meter_readings_id = 3
    response = await delete_meter_readings(meter_readings_id)
    response_dict = response.model_dump()

    mock_cursor.execute.assert_any_call('DELETE FROM meter_readings WHERE meter_readings_id = %s',
                                        (meter_readings_id,))
    mock_db.commit.assert_called_once_with()

    assert response_dict["status_code"] == 200
    assert "deleted successfully" in response_dict["message"]
