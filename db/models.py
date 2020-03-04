from sqlalchemy import Table, Column, Integer, Float, String, MetaData, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy	import create_engine
from sqlalchemy.ext.declarative import declarative_base
import datetime
import os
import random
from uuid import uuid4

engine = create_engine(os.environ["DATABASE_URL"], echo=True)

meta = MetaData()
Base = declarative_base()

class Entry(Base):
	__tablename__ = "entries"

	id = Column(Integer, primary_key=True, autoincrement=True)
	uuid = Column(UUID(as_uuid=True), default=uuid4)
	message = Column(String)
	date_created = Column(DateTime)
	date_modified = Column(DateTime)

	def create_entry(self, message):
		self.message = message
		self.date_created = datetime.datetime.now()
		self.date_modified = datetime.datetime.now()

	def __repr__(self):
		return "<Entry(id='%s', message='%s'" %(self.id, self.message)

if __name__ == '__main__':
	Base.metadata.create_all(engine)