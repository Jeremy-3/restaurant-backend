from sqlalchemy import Column,String,Integer,Boolean,TIMESTAMP,func,ForeignKey
from sqlalchemy.orm import relationship
from datetime import timezone,datetime
from app.db.base import Base
from sqlalchemy.dialects.postgresql import UUID 
import uuid

class RolePermission(Base):
    __tablename__ = "role_permissions"
    
    id = Column(Integer, primary_key=True)
    uid=Column(UUID(as_uuid=True),unique=True,default=uuid.uuid4,nullable=False,index=True)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    permissions_id = Column(Integer, ForeignKey('permissions.id'), nullable=False)
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), server_default=func.now(), nullable=False) # timezone = True ensures that the column is timezone-aware. # lambda function, ensures that a new timestamp is generated each time a record is created or updated.
    updated_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), server_default=func.now(), nullable=False)

    creator = relationship("User", foreign_keys=[created_by], back_populates="created_role_permissions")
    role = relationship("Roles", back_populates="role_permissions")
    permission = relationship("Permissions", back_populates="role_permissions")