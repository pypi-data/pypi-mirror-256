# Flask-AA

Flask extension for authentication and authorization.

It can be used as an alternative for Flask-Login.

Apart from base functionality for user session management it provides also routes for login (it renders auth/login.html template) and logout.
Users can be checked against external TACACS+ server (the Flask app config should have `TACACS_SERVER` and `TACACS_SECRET_KEY` keys).

There is also a UserMixin model class with the following fields (username, remote, password_hash, first_name, last_name, email, active, admin, created, last_login).


## Installation

```bash
$ pip install Flask-AA
```


## Usage

First create the `auth` object:

```python
from flask_auth import Auth
auth = Auth()
```

Then initialize it using init_app method:

```python
auth.init_app(app, db, User, wtf)
# app is your Flask app instance
# db is your Flask-Alchemist instance
# User is your User model
# wtf is your Flask-Formist instance for handling forms
```


## License

`Flask-AA` was created by Rafal Padkowski. It is licensed under the terms
of the MIT license.
