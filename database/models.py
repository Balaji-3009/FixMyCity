from sqlalchemy import Column, ForeignKey, Integer, String, Float
from database.session import Base
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Entry(Base):
    __tablename__ = 'entry'
    
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String)

class Profile(Base):
    
    __tablename__ = 'profile'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    uuid = Column(UUID(as_uuid=True), ForeignKey("entry.uuid"))
    email = Column(String)
    pno = Column(String)
    address = Column(String)
    
class Issues(Base):
    
    __tablename__ = 'issues'
    id = Column(Integer,primary_key=True,index=True)
    uuid = Column(UUID(as_uuid=True), ForeignKey("entry.uuid"))
    name = Column(String)
    image = Column(String)
    lat = Column(Float)
    long = Column(Float)
    description = Column(String)
    status = Column(Integer, default=0)