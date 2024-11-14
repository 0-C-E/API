import pytest
from flask import Flask


@pytest.fixture
def app():
    def create_app(blueprint):
        app = Flask(__name__)
        app.register_blueprint(blueprint, url_prefix=f"/{blueprint.name}")
        app.config["TESTING"] = True
        return app

    return create_app


@pytest.fixture
def client(app):
    def get_client(blueprint):
        return app(blueprint).test_client()

    return get_client


# Utility function to mock database responses
def mock_db_response(mock_get_db, data, fetchone=False):
    mock_cursor = mock_get_db.return_value.cursor.return_value.__enter__.return_value
    if fetchone:
        mock_cursor.fetchone.return_value = data
    else:
        mock_cursor.fetchall.return_value = data
