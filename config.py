class Config:
    MONGO_URI = (
        "mongodb+srv://erannir94:4KeXw3Y9gWKogJjL@cluster0.or4yrkc.mongodb.net/Shifter"
    )

    # Configuration for SQLAlchemy (SQL database)
    SQLALCHEMY_DATABASE_URI = "sqlite:///users.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking
