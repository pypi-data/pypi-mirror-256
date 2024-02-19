from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp


class Mixin:
    def password_field(self):
        return PasswordField(
            "Password",
            validators=[
                DataRequired(message="Missing password"),
                EqualTo("confirm_password", message="Passwords do not match"),
                Length(min=8, message="Password must be at least 8 characters long"),
                self.password_has_digit,
                self.password_has_symbol,
                self.password_has_uppercase_letter,
                self.password_has_lowercase_letter,
            ],
            render_kw={"placeholder": " "},
        )

    @staticmethod
    def confirm_password_field():
        return PasswordField(
            "Confirm password",
            validators=[
                DataRequired(message="Missing confirmed password"),
            ],
            render_kw={"placeholder": " "},
        )

    @staticmethod
    def first_name_field():
        return StringField(
            "First name",
            validators=[
                DataRequired(message="Missing first name"),
                Regexp("^[A-Za-z]*$", message="First name must have only letters"),
            ],
            render_kw={"placeholder": " ", "autocomplete": "off"},
        )

    @staticmethod
    def last_name_field():
        return StringField(
            "Last name",
            validators=[
                DataRequired(message="Missing last name"),
                Regexp("^[A-Za-z]*$", message="Last name must have only letters"),
            ],
            render_kw={"placeholder": " ", "autocomplete": "off"},
        )

    @staticmethod
    def email_field():
        return StringField(
            "Email",
            validators=[
                DataRequired(message="Missing email"),
                Length(max=64),
                Email(message="Invalid email address"),
            ],
            render_kw={"placeholder": " ", "autocomplete": "off"},
        )
