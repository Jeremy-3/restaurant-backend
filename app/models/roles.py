from sqlalchemy import Column,String,Integer,ForeignKey,TIMESTAMP,func,Boolean
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy.dialects.postgresql import UUID 
import uuid



class Roles(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    uid=Column(UUID(as_uuid=True),unique=True,default=uuid.uuid4,nullable=False,index=True)
    name = Column(String, unique=True)
    active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey('users.id'),nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), server_default=func.now(), nullable=False) # timezone = True ensures that the column is timezone-aware. # lambda function, ensures that a new timestamp is generated each time a record is created or updated.
    updated_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), server_default=func.now(), nullable=False)

    creator = relationship("User", foreign_keys=[created_by], back_populates="created_roles")
    role_permissions = relationship("RolePermission", back_populates="role")
    users = relationship("User", back_populates="role", foreign_keys="User.role_id")

    