import re
from unittest.mock import patch

import pytest

from app import app


@pytest.fixture
def client():
    return app.test_client()


@pytest.mark.parametrize(
    "fixed_time", ["12:34:56 01/01/2024", "23:59:59 31/12/2023", "00:00:00 01/01/2025"]
)
def test_get_time(client, fixed_time):
    with patch("time.strftime", return_value=fixed_time):
        response = client.get("/time")
        assert response.status_code == 200
        assert response.json == {"server_time": fixed_time}


def test_time_format(client):
    response = client.get("/time")
    assert response.status_code == 200
    time_str = response.json.get("server_time")
    assert re.match(r"\d{2}:\d{2}:\d{2} \d{2}/\d{2}/\d{4}", time_str)
