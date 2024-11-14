from unittest.mock import patch

from routes.island import islands_blueprint
from tests.conftest import mock_db_response


# Test get_all_islands endpoint
@patch("routes.island.get_db_connection")
def test_get_all_islands(mock_get_db, client):
    mock_db_response(
        mock_get_db, [{"id": 1, "name": "Island1"}, {"id": 2, "name": "Island2"}]
    )

    response = client(islands_blueprint).get("/islands")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == [{"id": 1, "name": "Island1"}, {"id": 2, "name": "Island2"}]


# Test get_island_by_id endpoint
@patch("routes.island.get_db_connection")
def test_get_island_by_id(mock_get_db, client):
    mock_db_response(mock_get_db, {"id": 1, "name": "Island1"}, fetchone=True)

    response = client(islands_blueprint).get("/islands/1")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == {"id": 1, "name": "Island1"}


# Test get_island_cities endpoint
@patch("routes.island.get_db_connection")
def test_get_island_cities(mock_get_db, client):
    mock_db_response(
        mock_get_db,
        [{"city_id": 101, "name": "CityA"}, {"city_id": 102, "name": "CityB"}],
    )

    response = client(islands_blueprint).get("/islands/1/cities")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == [
        {"city_id": 101, "name": "CityA"},
        {"city_id": 102, "name": "CityB"},
    ]
