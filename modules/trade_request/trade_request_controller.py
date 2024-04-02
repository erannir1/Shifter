from flask import abort
from pydantic import ValidationError
from flask_restful import reqparse, Resource

from database import mongodb, MongoCollections
from modules.shift.shift import Shift
from modules.trade_request.trade_request import TradeRequest
from modules.user.user import User
from tools.message_formatter import message_formatter


class TradeRequestController(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "user", type=dict, required=True, help="User data required"
        )
        self.parser.add_argument(
            "exchanging_shifts",
            type=list,
            required=True,
            help="Exchanging shifts data required",
        )
        self.parser.add_argument(
            "receiving_shifts", type=list, default=None, help="Receiving shifts data"
        )
        self.collection = getattr(
            mongodb.mongo.db, MongoCollections.TRADE_REQUESTS_COLLECTION
        )

    def put(self):
        try:
            # Parse request arguments
            args = self.parser.parse_args()
            # Validate and create TradeRequest object
            trade_request = TradeRequest(**args)

            # Save TradeRequest to database
            self.collection.insert_one(trade_request.dict())

            return {"message": "TradeRequest created successfully"}, 201
        except ValidationError as e:
            # Abort the request with a 400 error and custom error message
            abort(
                400,
                description=message_formatter(
                    f"{e.__class__.__name__} - {str(e)}", 500
                ),
            )
        except Exception as e:
            # Abort the request with a 500 error and custom error message
            abort(
                500,
                description=message_formatter(
                    f"{e.__class__.__name__} - {str(e)}", 500
                ),
            )
