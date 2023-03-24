from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Date
from .database import Base
from sqlalchemy.orm import relationship

class Blog(Base):
    __tablename__ = 'blogs'
    id  = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship("User", back_populates='blogs')

class User(Base):
    __tablename__ = 'users'
    id  = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    phone = Column(String, unique=True)
    birth_of_date = Column(Date)
    address = Column(String)
    status = Column(String(1))
    create_on = Column(DateTime)
    update_on = Column(DateTime)
    blogs = relationship("Blog", back_populates='creator')

class Blacklist(Base):
    __tablename__ = 'blacklists'
    id  = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    token = Column(String, unique=True)

class Code(Base):
    __tablename__ = 'codes'
    id  = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    reset_code = Column(String)
    expired_in = Column(DateTime)

class Otps(Base):
    __tablename__ = 'otps'
    id  = Column(Integer, primary_key=True, index=True)
    recipient_id = Column(String)
    session_id = Column(String)
    otp_code = Column(String(6))
    status = Column(String(1))
    create_on = Column(DateTime)
    update_on = Column(DateTime)
    otp_failed_count = Column(Integer, default=0)

class Optblocks(Base):
    __tablename__ = 'otp_block_lists'
    id  = Column(Integer, primary_key=True, index=True)
    recipient_id = Column(String)
    create_on = Column(DateTime)