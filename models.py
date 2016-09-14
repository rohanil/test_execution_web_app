from sqlalchemy import Column, Integer, String, DateTime, Text, Enum
from database import Base
from datetime import datetime


class Request(Base):
    __tablename__ = 'requests'

    id = Column(Integer, primary_key=True)
    environment_id = Column(Integer)
    requester = Column(String(80))
    created_at = Column(DateTime)
    template = Column(Text)
    status = Column(Enum('Running', 'Failed', 'Succeded'))
    stacktrace = Column(Text)

    def __init__(self, environment_id, requester, template, status,
                 created_at=None, stacktrace=None):
        self.environment_id = environment_id
        self.requester = requester
        self.template = template
        if created_at is None:
            created_at = datetime.utcnow()
        self.created_at = created_at
        self.status = status
        self.stacktrace = stacktrace

    def __repr__(self):
        return '<environment_id {}>'.format(self.environment_id)
