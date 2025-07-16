from sqlalchemy import Column,String,Boolean,Integer,TIMESTAMP,func,ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID,CITEXT
from datetime import datetime,timezone
from app.models.roles import Roles

class User(Base):
    __tablename__ = "users"
    
    id=Column(Integer,primary_key=True,index=True)
    uid=Column(UUID(as_uuid=True),unique=True,default=uuid.uuid4,nullable=False,index=True)
    name=Column(String,index=True)
    email = Column(String,unique=True, index=True) 
    password=Column(String)
    is_active=Column(Boolean,default=True)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), server_default=func.now(), nullable=False) # timezone = True ensures that the column is timezone-aware. # lambda function, ensures that a new timestamp is generated each time a record is created or updated.
    created_by = Column(Integer, ForeignKey('users.id'),nullable=True)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
   
    
    
    # relationship
    role = relationship("Roles", back_populates="users", foreign_keys=[role_id])
    permissions = relationship("Permissions", back_populates="creator")
    creator = relationship("User", remote_side=[id], back_populates="created_users")
    created_users = relationship("User", back_populates="creator")

    # created by this user
    created_roles = relationship("Roles", foreign_keys='Roles.created_by', back_populates="creator")
    created_role_permissions = relationship("RolePermission", back_populates="creator")

    
