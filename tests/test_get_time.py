import time

import pytest

from app import app


@pytest.fixture
def client():
    return app.test_client()


def test_get_time(client):
    response = client.get("/time")
    assert response.status_code == 200
    assert response.json == {"server_time": time.strftime("%H:%M:%S %d/%m/%Y")}
