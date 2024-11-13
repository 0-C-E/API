import datetime
import re
from unittest.mock import patch

import pytest

from app import app


@pytest.fixture
def client():
    return app.test_client()


@pytest.mark.parametrize(
    "fixed_time",
    [
        datetime.datetime(2024, 1, 1, 12, 34, 56),
        datetime.datetime(2023, 12, 31, 23, 59, 59),
        datetime.datetime(2025, 1, 1, 0, 0, 0),
    ],
)
def test_get_time(client, fixed_time):
    with patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = fixed_time
        response = client.get("/time")
        assert response.status_code == 200
        assert response.json == {
            "success": True,
            "data": {"server_time": fixed_time.isoformat()},
        }


def test_time_format(client):
    response = client.get("/time")
    assert response.status_code == 200
    time_str = response.json.get("data", {}).get("server_time")
    assert re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", time_str)
