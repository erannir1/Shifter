from typing import Tuple, List

from flask import abort
from pymongo.collection import Collection
from flask_restful import Resource, reqparse

from database import mongodb, MongoCollections
from tools.message_formatter import message_formatter
from modules.trade_request.trade_request import TradeRequest


class ControllerConfig:
    DEFAULT_PAGE_SIZE = 10
    PAGE = "page"


class RequestsFeedController(Resource):
    def __init__(self, *args, **kwargs):
        self.class_config = ControllerConfig
        self.collection: Collection = getattr(
            mongodb.db, MongoCollections.TRADE_REQUESTS_COLLECTION
        )
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(self.class_config.PAGE, type=int, default=1)
        super().__init__(*args, **kwargs)

    def get(self) -> Tuple[List[TradeRequest], int]:
        try:
            # Parse pagination parameters
            args = self.parser.parse_args()
            page = args[self.class_config.PAGE]
            page_size = self.class_config.DEFAULT_PAGE_SIZE
            skip = (page - 1) * page_size

            # Retrieve documents for the current page
            projection = {"_id": False}
            trade_requests = list(
                self.collection.find({}, projection).skip(skip).limit(page_size)
            )

            # If no documents are found, return an empty list
            if not trade_requests:
                return [], 200

            # Return the trade requests and HTTP status code 200 (OK)
            return trade_requests, 200

        except Exception as e:
            # abort request
            abort(
                500,
                description=message_formatter(
                    f"{e.__class__.__name__} - {str(e)}", 500
                ),
            )
