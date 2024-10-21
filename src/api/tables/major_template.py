from sqlalchemy import Column, PrimaryKeyConstraint

from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR, JSON

from .database import Base


class MajorTemplate(Base):
    __tablename__ = "major_template"

    major = Column(VARCHAR(length=4))
    year = Column(INTEGER)
    classes = Column(JSON, nullable=False)
    __table_args__ = (
        PrimaryKeyConstraint('major', 'year'),
    )

    def __repr__(self):
        return f"<MajorTemplate(major={self.major}, year={self.year}, classes={self.classes}"