import re

from flask import g
from flask_auxs import PermissionDenied
from wtforms.validators import DataRequired, Length, Regexp, ValidationError


class Mixin:
    def valid_username_and_password(self, form, _field):
        if not form.password.data:
            return

        username = form.username.data
        password = form.password.data

        g.user = self.authenticate(username, password)

        if not g.user:
            raise ValidationError("Invalid username or password")

    @staticmethod
    def username_input_required():
        return DataRequired(message="Missing username")

    @staticmethod
    def username_length():
        return Length(
            3, 64, message="Username must be between 3 and 64 characters long"
        )

    @staticmethod
    def username_regexp():
        return Regexp(
            "^[A-Za-z][A-Za-z0-9_.]*$",
            message="Username must begin with a letter "
            "and have only letters, numbers, dots or underscores",
        )

    def user_does_not_exist(self, form, _field):
        username = form.username.data

        user = self.get_user(username)

        if user:
            raise ValidationError("User exists")

    def new_username_does_not_exist(self, form, field):
        new_username = field.data

        if g.user.username == new_username:
            return

        self.user_does_not_exist(form, field)

    @staticmethod
    def password_has_digit(_form, field):
        password = field.data

        if not re.search(r"\d", password):
            raise ValidationError("Password should contain at least 1 digit")

    @staticmethod
    def password_has_symbol(_form, field):
        password = field.data

        if not re.search(r"\W", password):
            raise ValidationError("Password should contain at least 1 symbol")

    @staticmethod
    def password_has_uppercase_letter(_form, field):
        password = field.data

        if not re.search(r"[A-Z]", password):
            raise ValidationError("Password should contain at least 1 uppercase letter")

    @staticmethod
    def password_has_lowercase_letter(_form, field):
        password = field.data

        if not re.search(r"[a-z]", password):
            raise ValidationError("Password should contain at least 1 lowercase letter")

    @staticmethod
    def current_user_is_owner(obj):
        if g.user.id != obj.id:
            raise PermissionDenied
