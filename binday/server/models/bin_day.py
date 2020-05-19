from enum import Enum

from binday.server.factories.application import db
from binday.server.models.base import Base


class DayIndex(Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"


class CollectionFrequency(Enum):
    WEEKLY = "Weekly"
    FORTNIGHTLY = "Fortnightly"
    MONTHLY = "Monthly"


class BinDay(Base):
    __tablename__ = "bin_day"

    id = db.Column(db.Integer, primary_key=True)

    day_index = db.Column(db.Enum(DayIndex), nullable=False)
    frequency = db.Column(db.Enum(CollectionFrequency), nullable=False)

    def __repr__(self):
        return f"<BinDay {self.day_index, self.frequency}>"
