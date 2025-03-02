from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    
    fund_id = Column(Integer, ForeignKey("fund.id"), nullable=False)
    fund = relationship("Fund", backref="users")
    
    role = Column(String(50), nullable=False)  # admin, manager
    is_active = Column(Boolean, default=True)
    
    # Связи с другими таблицами
    created_players = relationship("Player", back_populates="created_by_user")
    created_cases = relationship("Case", back_populates="created_by_user")
    closed_cases = relationship("Case", back_populates="closed_by_user", foreign_keys="Case.closed_by_user_id")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()) 