from pydantic import ValidationError
from flask_restful import reqparse, Resource
from flask import abort, render_template, request
from flask_login import current_user, login_required

from modules.shift.shift import Shift
from database import mongodb, MongoCollections
from tools.message_formatter import message_formatter
from modules.trade_request.trade_request import TradeRequest


class TradeRequestController(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.collection = getattr(
            mongodb.db, MongoCollections.TRADE_REQUESTS_COLLECTION
        )

    @login_required
    def get(self):

        return render_template("create_request.html")

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

    @login_required
    def post(self):

        try:
            role: str = current_user.role
            company: str = current_user.company

            exchanging_shifts_data = request.form.getlist("exchanging_shifts")
            receiving_shifts_data = request.form.getlist("receiving_shifts")

            exchanging_shifts = self.parse_shifts(exchanging_shifts_data)
            receiving_shifts = self.parse_shifts(receiving_shifts_data)

            # Validate and create TradeRequest object
            trade_request = TradeRequest(
                company=company,
                role=role,
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

