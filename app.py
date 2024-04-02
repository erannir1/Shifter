import werkzeug
from loguru import logger
from flask_cors import CORS
from flask_restful import Api
from flask import Flask, jsonify

from cache import cache
from config import Config
from database import mongodb
from modules.requests_feed.requests_feed_controller import RequestsFeedController
from modules.trade_request.trade_request_controller import TradeRequestController
from modules.user.user_controller import UserController

app = Flask(__name__)

app.config.from_object(Config)
cache.init_app(app, config=app.config)
api = Api(app)
mongodb.init_app(app)
CORS(app)


@app.errorhandler(Exception)
def exceptions(e):
    logger.exception(e)
    return "Internal server error", 500


@app.errorhandler(werkzeug.exceptions.NotFound)
def handle_not_found(e):
    logger.exception(e)
    return jsonify({"message": e.description}), 404


@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    logger.exception(e)
    return jsonify({"message": e.description}), 400


@app.errorhandler(werkzeug.exceptions.InternalServerError)
def handle_internal_server_error(e):
    logger.exception(e)
    return jsonify({"message": e.description}), 500


@app.route("/health")
def health():
    return "OK"


@app.route("/")
def hello():
    return "Welcome To Shifter ;)"


api.add_resource(RequestsFeedController, "/requests_feed")
api.add_resource(TradeRequestController, "/trade_request")
api.add_resource(UserController, "/user")


if __name__ == "__main__":
    app.run(debug=True)
