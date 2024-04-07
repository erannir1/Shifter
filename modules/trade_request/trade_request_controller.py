from flask import abort
from pydantic import ValidationError
from flask_restful import reqparse, Resource

from modules.shift.shift import Shift
from database import mongodb, MongoCollections
from tools.message_formatter import message_formatter
from modules.trade_request.trade_request import TradeRequest


class TradeRequestController(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "company", type=str, required=True, help="Company name required"
        )
        self.parser.add_argument(
            "role",
            type=str,
            required=True,
            help="Role required",
        )
        self.parser.add_argument(
            "exchanging_shifts",
            type=dict,
            required=True,
            action="append",
            help="Exchanging shifts data required",
        )
        self.parser.add_argument(
            "receiving_shifts",
            type=dict,
            default=None,
            action="append",
            help="Receiving shifts data",
        )
        self.collection = getattr(
            mongodb.db, MongoCollections.TRADE_REQUESTS_COLLECTION
        )

    def parse_shifts(self, shifts_data):
        shifts = []
        for shift_data in shifts_data:
            try:
                shift = Shift(**shift_data)
                shifts.append(shift)
            except ValidationError as e:
                # Raise validation error if shift data is invalid
                abort(
                    400,
                    description=message_formatter(
                        f"Invalid shift data: {e.errors()}", 400
                    ),
                )
        return shifts

    def put(self):
        try:
            # Parse request arguments
            args = self.parser.parse_args()

            # Parse exchanging shifts
            exchanging_shifts = self.parse_shifts(args["exchanging_shifts"])

            # Parse receiving shifts if available
            receiving_shifts = self.parse_shifts(args.get("receiving_shifts", []))

            # Validate and create TradeRequest object
            trade_request = TradeRequest(
                company=args["company"],
                role=args["role"],
                exchanging_shifts=exchanging_shifts,
                receiving_shifts=receiving_shifts,
            )

            # Save TradeRequest to database
            self.collection.insert_one(trade_request.dict())

            return {"message": "TradeRequest created successfully"}, 201
        except Exception as e:
            # Abort the request with a 500 error and custom error message
            abort(
                500,
                description=message_formatter(f"Internal Server Error: {str(e)}", 500),
            )
