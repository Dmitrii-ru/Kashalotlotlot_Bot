
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from db.db_postgres_settings import Base
from sqlalchemy.orm import relationship, sessionmaker

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)

    currency_requests = relationship("UserCurrencyRequest", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, user_id={self.user_id}, username={self.username})>"