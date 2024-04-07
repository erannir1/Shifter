from flask_restful import Resource
from flask_login import login_user, current_user
from werkzeug.security import check_password_hash
from flask import request, flash, redirect, render_template

from modules.user.user import User


class UserLogin(Resource):
    def get(self):
        return render_template("login.html")

    def post(self):
        email = request.form.get("email")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("Please check your login details and try again.")
            return redirect("/auth/login")

        if current_user.is_authenticated:
            # If user is already authenticated, redirect to profile
            return redirect("/profile")

        login_user(user, remember=remember)
        return redirect("/profile")
