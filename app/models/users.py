from sqlalchemy import Boolean, Column, Integer, String, DateTime


from ..database.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), unique=True)
    public_id = Column(String(50), unique=True)
    firstname = Column(String(30), nullable=False)
    lastname = Column(String(30), nullable=False)
    email = Column(String(80), nullable=False, unique=True)
    password = Column(String(150), nullable=False)
    register_date = Column(DateTime, nullable=True)
    admin = Column(Boolean, default=False)
    confirmed = Column(Boolean, nullable=False, default=False)
    confirmed_on = Column(DateTime, nullable=True)
    disabled = Column(Boolean, nullable=True)
