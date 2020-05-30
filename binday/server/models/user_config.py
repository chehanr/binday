
from sqlalchemy.dialects.mysql import INTEGER

from binday.boards.board import BoardType
from binday.server.factories.application import db


class UserConfig(db.Model):
    __tablename__ = "user_config"

    pushbullet_api_key = db.Column(db.String(128))

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False,  primary_key=True)
    user = db.relationship("User", foreign_keys=user_id)

    def __repr__(self):
        return f"<UserConfig>"
