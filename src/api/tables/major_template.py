from sqlalchemy import Column, PrimaryKeyConstraint

from sqlalchemy.dialects.postgresql import INTEGER, TEXT, BOOLEAN, JSON

from .database import Base


class MajorTemplate(Base):
    __tablename__ = "major_template"

    major = Column(TEXT)
    year = Column(INTEGER) #year of entry
    school = Column(TEXT)
    credits = Column(INTEGER)
    focus_track = Column(BOOLEAN)
    link = Column(TEXT)
    notes = Column(JSON)
    required = Column(JSON)
    pick_multiple = Column(JSON)


    __table_args__ = (
        PrimaryKeyConstraint('major', 'year'),
    )

    def __repr__(self):
        return f"<MajorTemplate(major={self.major}, year={self.year})>"