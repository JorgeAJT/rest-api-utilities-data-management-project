import pytest
from src.meter_data import (
    get_meter_data_by_path_params,
    get_meter_data_by_query_params,
    post_meter_data, put_meter_data,
    delete_meter_data)
from src.models import MeterDataRequest


@pytest.fixture
def db_cursor_mock(mocker):
    mock_db = mocker.MagicMock()
    mock_cursor = mocker.MagicMock()

    mock_db.__enter__.return_value = mock_db
    mock_db.cursor.return_value.__enter__.return_value = mock_cursor

    return mock_db, mock_cursor


@pytest.mark.asyncio
async def test_get_meter_data_by_path_params(mocker, db_cursor_mock):
    expected_rows = [
        {
            "meter_data_id": 2,
            "meter_number": "000000005912273146",
            "connection_ean_code": "871694840015271748",
            "business_partner_id": "0100000022",
            "brand": "ES",
            "grid_company_code": "8716948000003",
            "oda_code": "8712423026766",
            "smart_collectable": "1",
            "sjv1": 301.0,
            "sjv2": None,
            "installation": "0801225660",
            "division": "02",
            "move_out_date": "2024-10-27T00:00:00",
            "row_create_datetime": "2024-08-09T07:38:07",
            "move_in_date": "2022-01-21T00:00:00"
        }
    ]

    mock_db, mock_cursor = db_cursor_mock
    mock_cursor.fetchall.return_value = expected_rows
    mocker.patch("src.meter_data.get.db_connection", return_value=mock_db)

    connection_ean_code = "871694840015271748"
    response = await get_meter_data_by_path_params(connection_ean_code)

    mock_cursor.execute.assert_called_once_with('SELECT * FROM meter_data WHERE connection_ean_code = %s',
                                                (connection_ean_code,))

    assert response.model_dump() == {"status_code": 200, "message": {"meter_data": expected_rows}}


@pytest.mark.asyncio
async def test_get_meter_data_by_query_params(mocker, db_cursor_mock):
    expected_rows = [
        {
            "meter_data_id": 3,
            "meter_number": "000000000032473417",
            "connection_ean_code": "871694840008930232",
            "business_partner_id": "0100000024",
            "brand": "ES",
            "grid_company_code": "8716948000003",
            "oda_code": "8712423026766",
            "smart_collectable": "1",
            "sjv1": 1313.0,
            "sjv2": 982.0,
            "installation": "0801859418",
            "division": "01",
            "move_out_date": "9999-12-31T00:00:00",
            "row_create_datetime": "2024-08-09T07:38:07",
            "move_in_date": "2015-12-10T00:00:00"
        }
    ]

    mock_db, mock_cursor = db_cursor_mock
    mock_cursor.fetchall.return_value = expected_rows
    mocker.patch("src.meter_data.get.db_connection", return_value=mock_db)

    business_partner_id = "0100000024"
    connection_ean_code = "871694840008930232"
    response = await get_meter_data_by_query_params(business_partner_id, connection_ean_code)

    mock_cursor.execute.assert_called_once_with('SELECT * FROM meter_data '
                                                'WHERE business_partner_id = %s AND connection_ean_code = %s',
                                                (business_partner_id, connection_ean_code))

    assert response.model_dump() == {"status_code": 200, "message": {"meter_data": expected_rows}}


@pytest.mark.asyncio
async def test_post_meter_data(mocker, db_cursor_mock):
    request_data = {
        "meter_number": "00000000003",
        "connection_ean_code": "871694840223121111",
        "business_partner_id": "010000007",
        "brand": "ES",
        "grid_company_code": "8716948000003",
        "oda_code": "8712423026766",
        "smart_collectable": "1",
        "sjv1": 1313.0,
        "sjv2": 982.0,
        "installation": "0801859418",
        "division": "01",
        "move_out_date": "9999-12-31T00:00:00",
        "row_create_datetime": "2024-08-09T07:38:07",
        "move_in_date": "2015-12-10T00:00:00"
    }

    meter_data_request = MeterDataRequest(**request_data)

    mock_db, mock_cursor = db_cursor_mock
    mock_cursor.fetchone.return_value = (90,)
    mocker.patch("src.meter_data.post.db_connection", return_value=mock_db)

    response = await post_meter_data(meter_data_request)

    expected_query = ("INSERT INTO meter_data "
                      "(meter_number, connection_ean_code, business_partner_id, brand, "
                      "grid_company_code, oda_code, smart_collectable, sjv1, sjv2, installation, "
                      "division, move_out_date, row_create_datetime, move_in_date) "
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                      "RETURNING meter_data_id")

    expected_params = tuple(meter_data_request.model_dump().values())

    mock_cursor.execute.assert_called_once_with(expected_query, expected_params)
    mock_db.commit.assert_called_once_with()

    expected_response = {
        "status_code": 201,
        "message": {
            "meter_data": {
                "meter_data_id": 90,
                **meter_data_request.model_dump()
            }
        }
    }

    assert response.model_dump() == expected_response


@pytest.mark.asyncio
async def test_put_meter_data(mocker, db_cursor_mock):
    request_data = {
        "meter_number": "000000000000563653",
        "connection_ean_code": "871694840007526085",
        "business_partner_id": "0100000314",
        "brand": "ES",
        "grid_company_code": "8716948000003",
        "oda_code": "8712423026766",
        "smart_collectable": "1",
        "sjv1": 2448.0,
        "sjv2": 1404.0,
        "installation": "0801225258",
        "division": "01",
        "move_out_date": "9999-12-31T00:00:00",
        "row_create_datetime": "2024-08-09T07:38:07",
        "move_in_date": "2009-12-17T00:00:00"
    }

    meter_data_request = MeterDataRequest(**request_data)

    mock_db, mock_cursor = db_cursor_mock
    mocker.patch("src.meter_data.put.db_connection", return_value=mock_db)

    meter_data_id = 82
    response = await put_meter_data(meter_data_id, meter_data_request)

    expected_query = ("UPDATE meter_data "
                      "SET meter_number = %s, "
                      "connection_ean_code = %s, "
                      "business_partner_id = %s, "
                      "brand = %s, "
                      "grid_company_code = %s, "
                      "oda_code = %s, "
                      "smart_collectable = %s, "
                      "sjv1 = %s, sjv2 = %s, "
                      "installation = %s, "
                      "division = %s, "
                      "move_out_date = %s, "
                      "row_create_datetime = %s, "
                      "move_in_date = %s "
                      "WHERE meter_data_id = %s")

    expected_params = tuple(meter_data_request.model_dump().values()) + (meter_data_id,)

    mock_cursor.execute.assert_any_call(expected_query, expected_params)
    mock_db.commit.assert_called_once_with()

    expected_response = {
        "status_code": 201,
        "message": {
            "meter_data": {
                "meter_data_id": meter_data_id,
                **meter_data_request.model_dump()
            }
        }
    }

    assert response.model_dump() == expected_response


@pytest.mark.asyncio
async def test_delete_meter_data(mocker, db_cursor_mock):
    mock_db, mock_cursor = db_cursor_mock
    mocker.patch("src.meter_data.delete.db_connection", return_value=mock_db)

    meter_data_id = 82
    response = await delete_meter_data(meter_data_id)
    response_dict = response.model_dump()

    mock_cursor.execute.assert_any_call('DELETE FROM meter_data WHERE meter_data_id = %s',
                                        (meter_data_id,))
    mock_db.commit.assert_called_once_with()

    assert response_dict["status_code"] == 200
    assert "deleted successfully" in response_dict["message"]
