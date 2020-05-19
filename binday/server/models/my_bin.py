
from sqlalchemy.dialects.mysql import INTEGER

from binday.boards.board import BoardType
from binday.server.factories.application import db
from binday.server.models.base import Base


class MyBin(Base):
    __tablename__ = "my_bin"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(128))

    color_hex = db.Column(db.String(7), nullable=False)
    capacity = db.Column(INTEGER(unsigned=True), nullable=False)
    height = db.Column(INTEGER(unsigned=True), nullable=False)

    board_type = db.Column(db.Enum(BoardType), nullable=False)
    device_name = db.Column(db.String(32), nullable=False)
    sonar_id = db.Column(db.String(32), nullable=False)
    led_id = db.Column(db.String(32), nullable=False)

    creator_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    creator = db.relationship("User", foreign_keys=creator_id)
    bin_day_id = db.Column(db.Integer, db.ForeignKey("bin_day.id"), nullable=False)
    bin_day = db.relationship("BinDay", foreign_keys=bin_day_id)


    def __repr__(self):
        return f"<MyBin {self.name}>"
