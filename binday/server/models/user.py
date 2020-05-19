from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from binday.server.factories.application import db, login_manager
from binday.server.models.base import Base


class User(UserMixin, Base):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
