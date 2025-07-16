import os

def get_db():
    if os.getenv('APP_ENV') == "local":
         from app.db.local_connection import DB_Session
    else:
        from app.db.local_connection import DB_Session
        
    db = DB_Session()
    try:
        yield db         
    finally:
        db.close()    