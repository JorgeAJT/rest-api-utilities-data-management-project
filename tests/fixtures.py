import pytest
import os


@pytest.fixture
def db_cursor_mock(mocker):
    mock_db = mocker.MagicMock()
    mock_cursor = mocker.MagicMock()

    mock_db.__enter__.return_value = mock_db
    mock_db.cursor.return_value.__enter__.return_value = mock_cursor

    return mock_db, mock_cursor


@pytest.fixture(scope="session")
def environmental_variables():
    os.environ["dbname"] = "testing_db"
    os.environ["user"] = "postgres"
    os.environ["password"] = "testing1234"
    os.environ["host"] = "testing-db"
    os.environ["port"] = "5433"

    return True
