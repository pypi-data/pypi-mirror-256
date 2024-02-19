from datetime import datetime, timezone

import sqlalchemy as sa
from flask import Blueprint, flash, g, redirect, session
from flask_auxs import get_cancel, get_next
from tacacs_plus.client import TACACSClient

from . import fields, forms, validators


class Auth(forms.Mixin, fields.Mixin, validators.Mixin):
    def __init__(self, app=None, db=None, UserModel=None, wtf=None):
        self.tacacs_client = None
        self.db = None
        self.UserModel = None
        self.wtf = None

        if (
            app is not None
            and db is not None
            and UserModel is not None
            and wtf is not None
        ):
            self.init_app(app, db, UserModel, wtf)

    def init_app(self, app, db, UserModel, wtf):
        tacacs_server = app.config.get("TACACS_SERVER")
        tacacs_secret_key = app.config.get("TACACS_SECRET_KEY")
        self.tacacs_client = TACACSClient(tacacs_server, 49, tacacs_secret_key)

        self.db = db
        self.UserModel = UserModel

        self.wtf = wtf

        blueprint = Blueprint("auth", __name__, url_prefix="/auth")

        @blueprint.route("/login/", methods=("GET", "POST"))
        def login():
            return self.wtf.handle_form(
                form_cls=self.get_login_form(),
                template="auth/login.html",
                on_success=on_login_success,
                cancel_url=get_cancel(),
            )

        def on_login_success(_form):
            login_user()

            flash(f"Successfully logged in as {g.user.username}", "success")
            return redirect(get_next())

        def login_user():
            session.clear()
            session["user_id"] = g.user.id

            with self.db.Session() as db_session, db_session.begin():
                user = db_session.get(self.UserModel, g.user.id)
                user.last_login = datetime.now(timezone.utc)

        @blueprint.route("/logout/")
        def logout():
            logout_user()

            flash("You have been logged out", "success")
            return redirect(get_next())

        def logout_user():
            session.clear()

        ##

        app.register_blueprint(blueprint)

        @app.before_request
        def load_user():
            user_id = session.get("user_id")

            if user_id is None:
                g.user = None
            else:
                with self.db.Session() as db_session:
                    user = db_session.get(self.UserModel, user_id)

                if user and user.is_active:
                    g.user = user
                else:
                    g.user = None

    def get_user(self, username):
        query = sa.select(self.UserModel).where(self.UserModel.username == username)
        with self.db.Session() as db_session:
            user = db_session.scalar(query)

        return user

    def authenticate(self, username, password):
        user = self.get_user(username)

        if user and user.is_active:
            if user.is_remote:
                authentication_reply = self.tacacs_client.authenticate(
                    username, password
                )
                if authentication_reply.valid:
                    return user
            else:
                if user.correct_password(password):
                    return user
        return None
