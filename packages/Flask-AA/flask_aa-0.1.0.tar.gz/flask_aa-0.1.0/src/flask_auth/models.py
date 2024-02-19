from datetime import datetime, timezone

import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash, generate_password_hash


class UserMixin:
    __tablename__ = "users"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    remote: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)

    username: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(162), nullable=True)

    first_name: so.Mapped[str] = so.mapped_column(sa.String(64))
    last_name: so.Mapped[str] = so.mapped_column(sa.String(64))

    email: so.Mapped[str] = so.mapped_column(sa.String(64), default="")

    active: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=True)
    admin: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)

    created: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    last_login: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=True)

    def __repr__(self):
        return self.name

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def correct_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_remote(self):
        return self.remote

    @hybrid_property
    def name(self):
        return self.last_name + " " + self.first_name

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin
