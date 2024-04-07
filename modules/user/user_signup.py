from flask_restful import Resource
from flask_login import current_user
from werkzeug.security import generate_password_hash
from flask import request, flash, redirect, url_for, render_template

from database import sqlalchemy_db
from modules.user.user import User


class UserSignup(Resource):
    def get(self):
        return render_template("signup.html", current_user=current_user)

    def post(self):
        email = request.form.get("email")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        password = request.form.get("password")
        company = request.form.get("company")

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email address already exists")
            return redirect("auth/signup")

        new_user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=generate_password_hash(password, method="sha256"),
            company=company,
        )
        sqlalchemy_db.session.add(new_user)
        sqlalchemy_db.session.commit()

        return redirect(url_for("auth.login"))
