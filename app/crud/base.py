from fastapi import status,HTTPException
from typing import Type,TypeVar,Generic
from sqlalchemy.orm import Session
from pydantic import BaseModel
import logging
from sqlalchemy import and_
# Define a generic model and schema
ModelType = TypeVar("ModelType")
SchemaType = TypeVar("SchemaType",bound=BaseModel)

# Configure logging
logger = logging.getLogger(__name__)

class CRUDBase(Generic[ModelType,SchemaType]):
    def __init__(self,model:Type[ModelType]):
        self.model= model
        
    def get_record_by_field(self,db:Session,field:str,value):
        if not hasattr(self.model,field):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Invalid Filed:{field}")
            
        column = getattr(self.model,field)
        record = db.query(self.model).filter(column == value).first()
            
        return record
         
    def get_record_by_fields(self, db: Session, filters: dict):
        invalid_fields = [f for f in filters if not hasattr(self.model, f)]
        if invalid_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid field(s): {', '.join(invalid_fields)}"
            )

        conditions = [getattr(self.model, field) == value for field, value in filters.items()]
        return db.query(self.model).filter(and_(*conditions)).first()
        
    def create_record(self,db:Session,record_create):
        #Create and save record
        record = self.model(**record_create.model_dump())
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
    
    def read_records(self,db:Session,page:int=1,limit:int =10):
        if page < 1 or limit < 1 :
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Page and limit must be positive integers."
            )
        offset = (page - 1) * limit
        query = db.query(self.model)
        records = query.offset(offset).limit(limit).all()
        total = query.count()
        return records, total

    def update_record(self,db: Session,record,record_in):
        update_data = record_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(record, field, value)

        db.commit()
        db.refresh(record)
        return record
            