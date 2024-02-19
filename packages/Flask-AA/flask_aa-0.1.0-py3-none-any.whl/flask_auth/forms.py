from wtforms import PasswordField, StringField
from wtforms.validators import InputRequired


class Mixin:
    def get_login_form(self):
        class LoginForm(self.wtf.BaseForm):
            username = StringField(
                "Username",
                validators=[
                    InputRequired(message="Missing username"),
                    self.valid_username_and_password,
                ],
                render_kw={"placeholder": " ", "autocomplete": "off"},
            )
            password = PasswordField(
                "Password",
                validators=[
                    InputRequired(message="Missing password"),
                ],
                render_kw={"placeholder": " "},
            )

        return LoginForm

    def get_register_form(self):
        class RegisterForm(self.wtf.BaseForm):
            username = StringField(
                "Username",
                validators=[
                    self.username_input_required,
                    self.username_length,
                    self.username_regexp,
                    self.user_does_not_exist,
                ],
                render_kw={"placeholder": " ", "autocomplete": "off"},
            )
            password = self.password_field()
            confirm_password = self.confirm_password_field()
            first_name = self.first_name_field()
            last_name = self.last_name_field()
            email = self.email_field()

        return RegisterForm

    def get_profile_form(self):
        class ProfileForm(self.wtf.BaseForm):
            username = StringField(
                "Username",
                validators=[
                    self.username_input_required,
                    self.username_length,
                    self.username_regexp,
                    self.new_username_does_not_exist,
                ],
            )
            first_name = self.first_name_field()
            last_name = self.last_name_field()
            email = self.email_field()

        return ProfileForm

    def get_password_form(self):
        class PasswordForm(self.wtf.BaseForm):
            password = self.password_field()
            confirm_password = self.confirm_password_field()

        return PasswordForm
