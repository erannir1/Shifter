import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask_restful import Api
from modules.trade_request.trade_request_controller import TradeRequestController
from database import mongodb  # Import the init_databases function


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/testdb"  # Set MongoDB test URI
    app.config["TESTING"] = True  # Enable testing mode
    mongodb.init_app(app)
    api = Api(app)
    api.add_resource(TradeRequestController, "/trade_request")
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_create_trade_request(client: FlaskClient):
    data = {
        "company": "Example Company",
        "role": "Example Role",
        "exchanging_shifts": [
            {
                "qualification": "Example Qualification",
                "start_time": "2024-04-07T09:00:00",
                "end_time": "2024-04-07T17:00:00",
            }
        ],
        "receiving_shifts": [
            {
                "qualification": "Example Qualification",
                "start_time": "2024-04-08T09:00:00",
                "end_time": "2024-04-08T17:00:00",
            }
        ],
    }

    response = client.put("/trade_request", json=data)
    assert response.status_code == 201
    assert response.json == {"message": "TradeRequest created successfully"}
