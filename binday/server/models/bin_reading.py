from enum import Enum

from binday.server.factories.application import db
from binday.server.models.base import Base


class BinReading(Base):
    __tablename__ = "bin_reading"

    id = db.Column(db.Integer, primary_key=True)
    sonar_reading = db.Column(db.Integer, nullable=False)
    led_status = db.Column(db.Boolean, nullable=False)

    my_bin_id = db.Column(db.Integer, db.ForeignKey("my_bin.id"), nullable=False)
    my_bin = db.relationship("MyBin", foreign_keys=my_bin_id)

    def __repr__(self):
        return f"<BinReading {self.my_bin.id , self.date_created}>"
