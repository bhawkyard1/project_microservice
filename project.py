from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Project(Base):
    __tablename__ = "project"
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    path = Column(String)

    def __repr__(self):
        return f"{self.name}, location: {self.path}"
