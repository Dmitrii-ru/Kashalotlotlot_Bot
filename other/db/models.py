from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from db.db_postgres_settings import Base


class Currency(Base):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    count = Column(Integer,default=0)
    currency_requests = relationship("UserCurrencyRequest", back_populates="currency")

    def __repr__(self):
        return f"<Currency(id={self.id}, code={self.code})>"



class UserCurrencyRequest(Base):
    __tablename__ = 'user_currency_requests'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    currency_id = Column(Integer, ForeignKey('currencies.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="currency_requests")
    currency = relationship("Currency", back_populates="currency_requests")

    def __repr__(self):
        return f"<UserCurrencyRequest(user_id={self.user_id}, currency_id={self.currency_id}, timestamp={self.timestamp})>"
