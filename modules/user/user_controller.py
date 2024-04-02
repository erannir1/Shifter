from flask import abort
from flask_restful import reqparse, Resource
from werkzeug.security import generate_password_hash


from modules.user.user import User
from database import mongodb, MongoCollections
from tools.message_formatter import message_formatter


class UserController(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "email", type=str, required=True, help="Email is required"
        )
        self.parser.add_argument(
            "password", type=str, required=True, help="Password is required"
        )
        self.parser.add_argument(
            "company", type=str, required=True, help="Company name is required"
        )
        self.collection = getattr(mongodb.mongo.db, MongoCollections.USERS_COLLECTION)

    def post(self):
        try:
            # Parse request arguments
            args = self.parser.parse_args()
            user = User(**args)

            # Check if email already exists
            existing_user = self.collection.find_one({"email": args["email"]})
            if existing_user:
                abort(400, description="User with this email already exists")

            # Hash the password
            hashed_password = generate_password_hash(args["password"])

            # Insert new user into MongoDB
            new_user = User(
                email=args["email"], password=hashed_password, company=args["company"]
            )

            user_id = self.collection.insert_one(new_user.dict).inserted_id

            return {
                "message": "User registered successfully",
                "user_id": str(user_id),
            }, 201

        except Exception as e:
            abort(
                500,
                description=message_formatter(
                    f"{e.__class__.__name__} - {str(e)}", 500
                ),
            )

    def get(self):
        try:
            return {"message": "Render the registration form in the app."}, 200

        except Exception as e:
            abort(
                500,
                description=message_formatter(
                    f"{e.__class__.__name__} - {str(e)}", 500
                ),
            )
