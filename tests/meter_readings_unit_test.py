import pytest
from src.meter_readings import (
    get_meter_readings_by_path_params,
    get_meter_readings_by_query_params)


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

    assert response.dict() == {"status_code": 200, "message": {"meter_readings": fake_rows}}


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

    assert response.dict() == {"status_code": 200, "message": {"meter_readings": fake_rows}}
