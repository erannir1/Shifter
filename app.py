import werkzeug
from loguru import logger
from flask_cors import CORS
from flask_restful import Api
from flask import Flask, jsonify, render_template
from flask_login import login_required, current_user, LoginManager

from cache import cache
from config import Config
from modules.user.user import User
from database import mongodb, sqlalchemy_db

from modules.user.user_login import UserLogin
from modules.user.user_logout import UserLogout
from modules.user.user_signup import UserSignup
from modules.requests_feed.requests_feed_controller import RequestsFeedController
from modules.trade_request.trade_request_controller import TradeRequestController


app = Flask(__name__)

app.config.from_object(Config)
cache.init_app(app, config=app.config)

mongodb.init_app(app)
sqlalchemy_db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

api = Api(app)
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
def index():
    return render_template("index.html", current_user=current_user)


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name=current_user.first_name)


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/login")
def login():
    return render_template("login.html")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


with app.app_context():
    sqlalchemy_db.create_all()


api.add_resource(RequestsFeedController, "/requests_feed")
api.add_resource(TradeRequestController, "/trade_request")
api.add_resource(UserLogin, "/login")
api.add_resource(UserSignup, "/signup")
api.add_resource(UserLogout, "/logout")


if __name__ == "__main__":
    app.run(debug=True)
