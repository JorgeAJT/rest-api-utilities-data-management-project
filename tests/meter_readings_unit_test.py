import pytest
from src.meter_readings import (
    get_meter_readings_by_path_params,
    get_meter_readings_by_query_params,
    post_meter_readings, put_meter_readings,
    delete_meter_readings)
from src.models import MeterReadingsRequest


@pytest.fixture
def db_cursor_mock(mocker):
    mock_cursor = mocker.MagicMock()
    mock_db = mocker.MagicMock()

    mock_db.__enter__.return_value = mock_db
    mock_db.cursor.return_value.__enter__.return_value = mock_cursor

    return mock_db, mock_cursor


@pytest.mark.asyncio
async def test_get_meter_readings_by_path_params(mocker, db_cursor_mock):
    fake_rows = [
        {
            "meter_readings_id": 3,
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
        },
        {
            "meter_readings_id": 87,
            "meter_number": "55933",
            "connection_ean_code": "871694840008583575",
            "account_id": "0100000025",
            "brand": "ESSENT",
            "energy_type": "ELECTRICITY",
            "reading_date": "2024-01-01",
            "reading_electricity": "{\"supplyLow\": 8376.55, \"supplyHigh\": 13001.778, "
                                   "\"returnLow\": 0.0, \"returnHigh\": 0.0}",
            "reading_gas": None,
            "rejection": None,
            "validation_status": "VALID"
        },
        {
            "meter_readings_id": 178,
            "meter_number": "55933",
            "connection_ean_code": "871694840008583575",
            "account_id": "0100000025",
            "brand": "ESSENT",
            "energy_type": "ELECTRICITY",
            "reading_date": "2024-02-01",
            "reading_electricity": "{\"supplyLow\": 8429.463, \"supplyHigh\": 13123.843, "
                                   "\"returnLow\": 0.0, \"returnHigh\": 0.0}",
            "reading_gas": None,
            "rejection": None,
            "validation_status": "VALID"
        },
        {
            "meter_readings_id": 282,
            "meter_number": "55933",
            "connection_ean_code": "871694840008583575",
            "account_id": "0100000025",
            "brand": "ESSENT",
            "energy_type": "ELECTRICITY",
            "reading_date": "2024-03-01",
            "reading_electricity": "{\"supplyLow\": 8475.562, \"supplyHigh\": 13241.289, "
                                   "\"returnLow\": 0.0, \"returnHigh\": 0.0}",
            "reading_gas": None,
            "rejection": None,
            "validation_status": "VALID"
        },
        {
            "meter_readings_id": 320,
            "meter_number": "55933",
            "connection_ean_code": "871694840008583575",
            "account_id": "0100000025",
            "brand": "ESSENT",
            "energy_type": "ELECTRICITY",
            "reading_date": "2023-12-01",
            "reading_electricity": "{\"supplyLow\": 8297.963, \"supplyHigh\": 12902.453, "
                                   "\"returnLow\": 0.0, \"returnHigh\": 0.0}",
            "reading_gas": None,
            "rejection": None,
            "validation_status": "VALID"
        },
        {
            "meter_readings_id": 467,
            "meter_number": "55933",
            "connection_ean_code": "871694840008583575",
            "account_id": "0100000025",
            "brand": "ESSENT",
            "energy_type": "ELECTRICITY",
            "reading_date": "2024-04-01",
            "reading_electricity": "{\"returnLow\": 0.0, \"supplyLow\": 8542.513, "
                                   "\"returnHigh\": 0.0, \"supplyHigh\": 13342.347}",
            "reading_gas": None,
            "rejection": None,
            "validation_status": "VALID"
        },
        {
            "meter_readings_id": 590,
            "meter_number": "55933",
            "connection_ean_code": "871694840008583575",
            "account_id": "0100000025",
            "brand": "ESSENT",
            "energy_type": "ELECTRICITY",
            "reading_date": "2024-05-01",
            "reading_electricity": "{\"returnLow\": 0.0, \"supplyLow\": 8597.069, "
                                   "\"returnHigh\": 0.0, \"supplyHigh\": 13431.77}",
            "reading_gas": None,
            "rejection": None,
            "validation_status": "VALID"
        },
        {
            "meter_readings_id": 671,
            "meter_number": "55933",
            "connection_ean_code": "871694840008583575",
            "account_id": "0100000025",
            "brand": "ESSENT",
            "energy_type": "ELECTRICITY",
            "reading_date": "2024-06-01",
            "reading_electricity": "{\"returnLow\": 0.0, \"supplyLow\": 8658.028, "
                                   "\"returnHigh\": 0.0, \"supplyHigh\": 13535.067}",
            "reading_gas": None,
            "rejection": None,
            "validation_status": "VALID"
        },
        {
            "meter_readings_id": 765,
            "meter_number": "55933",
            "connection_ean_code": "871694840008583575",
            "account_id": "0100000025",
            "brand": "ESSENT",
            "energy_type": "ELECTRICITY",
            "reading_date": "2024-07-01",
            "reading_electricity": "{\"returnLow\": 0.0, \"supplyLow\": 8724.639, "
                                   "\"returnHigh\": 0.0, \"supplyHigh\": 13620.487}",
            "reading_gas": None,
            "rejection": None,
            "validation_status": "VALID"
        },
        {
            "meter_readings_id": 853,
            "meter_number": "55933",
            "connection_ean_code": "871694840008583575",
            "account_id": "0100000025",
            "brand": "ESSENT",
            "energy_type": "ELECTRICITY",
            "reading_date": "2024-08-01",
            "reading_electricity": "{\"returnLow\": 0.0, \"supplyLow\": 8784.888, "
                                   "\"returnHigh\": 0.0, \"supplyHigh\": 13727.324}",
            "reading_gas": None,
            "rejection": None,
            "validation_status": "VALID"
        }
    ]

    mock_db, mock_cursor = db_cursor_mock
    mock_cursor.fetchall.return_value = fake_rows
    mocker.patch("src.meter_readings.get.db_connection", return_value=mock_db)

    connection_ean_code = "871694840008583575"
    response = await get_meter_readings_by_path_params(connection_ean_code)

    mock_cursor.execute.assert_called_once_with('SELECT * FROM meter_readings WHERE connection_ean_code = %s',
                                                (connection_ean_code,))

    assert response.model_dump() == {"status_code": 200, "message": {"meter_readings": fake_rows}}


@pytest.mark.asyncio
async def test_get_meter_readings_by_query_params(mocker, db_cursor_mock):
    fake_rows = [
        {
            "meter_readings_id": 3,
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
        },
        {
            "meter_readings_id": 87,
            "meter_number": "55933",
            "connection_ean_code": "871694840008583575",
            "account_id": "0100000025",
            "brand": "ESSENT",
            "energy_type": "ELECTRICITY",
            "reading_date": "2024-01-01",
            "reading_electricity": "{\"supplyLow\": 8376.55, \"supplyHigh\": 13001.778, "
                                   "\"returnLow\": 0.0, \"returnHigh\": 0.0}",
            "reading_gas": None,
            "rejection": None,
            "validation_status": "VALID"
        },
        {
            "meter_readings_id": 178,
            "meter_number": "55933",
            "connection_ean_code": "871694840008583575",
            "account_id": "0100000025",
            "brand": "ESSENT",
            "energy_type": "ELECTRICITY",
            "reading_date": "2024-02-01",
            "reading_electricity": "{\"supplyLow\": 8429.463, \"supplyHigh\": 13123.843, "
                                   "\"returnLow\": 0.0, \"returnHigh\": 0.0}",
            "reading_gas": None,
            "rejection": None,
            "validation_status": "VALID"
        },
        {
            "meter_readings_id": 282,
            "meter_number": "55933",
            "connection_ean_code": "871694840008583575",
            "account_id": "0100000025",
            "brand": "ESSENT",
            "energy_type": "ELECTRICITY",
            "reading_date": "2024-03-01",
            "reading_electricity": "{\"supplyLow\": 8475.562, \"supplyHigh\": 13241.289, "
                                   "\"returnLow\": 0.0, \"returnHigh\": 0.0}",
            "reading_gas": None,
            "rejection": None,
            "validation_status": "VALID"
        },
        {
            "meter_readings_id": 320,
            "meter_number": "55933",
            "connection_ean_code": "871694840008583575",
            "account_id": "0100000025",
            "brand": "ESSENT",
            "energy_type": "ELECTRICITY",
            "reading_date": "2023-12-01",
            "reading_electricity": "{\"supplyLow\": 8297.963, \"supplyHigh\": 12902.453, "
                                   "\"returnLow\": 0.0, \"returnHigh\": 0.0}",
            "reading_gas": None,
            "rejection": None,
            "validation_status": "VALID"
        },
        {
            "meter_readings_id": 467,
            "meter_number": "55933",
            "connection_ean_code": "871694840008583575",
            "account_id": "0100000025",
            "brand": "ESSENT",
            "energy_type": "ELECTRICITY",
            "reading_date": "2024-04-01",
            "reading_electricity": "{\"returnLow\": 0.0, \"supplyLow\": 8542.513, "
                                   "\"returnHigh\": 0.0, \"supplyHigh\": 13342.347}",
            "reading_gas": None,
            "rejection": None,
            "validation_status": "VALID"
        },
        {
            "meter_readings_id": 590,
            "meter_number": "55933",
            "connection_ean_code": "871694840008583575",
            "account_id": "0100000025",
            "brand": "ESSENT",
            "energy_type": "ELECTRICITY",
            "reading_date": "2024-05-01",
            "reading_electricity": "{\"returnLow\": 0.0, \"supplyLow\": 8597.069, "
                                   "\"returnHigh\": 0.0, \"supplyHigh\": 13431.77}",
            "reading_gas": None,
            "rejection": None,
            "validation_status": "VALID"
        },
        {
            "meter_readings_id": 671,
            "meter_number": "55933",
            "connection_ean_code": "871694840008583575",
            "account_id": "0100000025",
            "brand": "ESSENT",
            "energy_type": "ELECTRICITY",
            "reading_date": "2024-06-01",
            "reading_electricity": "{\"returnLow\": 0.0, \"supplyLow\": 8658.028, "
                                   "\"returnHigh\": 0.0, \"supplyHigh\": 13535.067}",
            "reading_gas": None,
            "rejection": None,
            "validation_status": "VALID"
        },
        {
            "meter_readings_id": 765,
            "meter_number": "55933",
            "connection_ean_code": "871694840008583575",
            "account_id": "0100000025",
            "brand": "ESSENT",
            "energy_type": "ELECTRICITY",
            "reading_date": "2024-07-01",
            "reading_electricity": "{\"returnLow\": 0.0, \"supplyLow\": 8724.639, "
                                   "\"returnHigh\": 0.0, \"supplyHigh\": 13620.487}",
            "reading_gas": None,
            "rejection": None,
            "validation_status": "VALID"
        },
        {
            "meter_readings_id": 853,
            "meter_number": "55933",
            "connection_ean_code": "871694840008583575",
            "account_id": "0100000025",
            "brand": "ESSENT",
            "energy_type": "ELECTRICITY",
            "reading_date": "2024-08-01",
            "reading_electricity": "{\"returnLow\": 0.0, \"supplyLow\": 8784.888, "
                                   "\"returnHigh\": 0.0, \"supplyHigh\": 13727.324}",
            "reading_gas": None,
            "rejection": None,
            "validation_status": "VALID"
        }
    ]

    mock_db, mock_cursor = db_cursor_mock
    mock_cursor.fetchall.return_value = fake_rows
    mocker.patch("src.meter_readings.get.db_connection", return_value=mock_db)

    account_id = "0100000025"
    connection_ean_code = "871694840008583575"
    response = await get_meter_readings_by_query_params(account_id, connection_ean_code)

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM meter_readings WHERE account_id = %s AND connection_ean_code = %s",
        (account_id, connection_ean_code)
    )

    assert response.model_dump() == {"status_code": 200, "message": {"meter_readings": fake_rows}}


@pytest.mark.asyncio
async def test_post_meter_readings(mocker, db_cursor_mock):
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
            "meter_readings": {
                "meter_readings_id": 100,
                **meter_readings_request.model_dump()
            }
        }
    }

    assert response.model_dump() == expected_response


@pytest.mark.asyncio
async def test_put_meter_readings(mocker, db_cursor_mock):
    request_data = {
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
            "meter_readings": {
                "meter_readings_id": meter_readings_id,
                **meter_readings_request.model_dump()
            }
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

    assert response_dict["status_code"] == 200
    assert "deleted successfully" in response_dict["message"]
