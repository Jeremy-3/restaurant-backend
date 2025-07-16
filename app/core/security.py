from passlib.context import CryptContext
from jose import jwt,JWTError
from datetime import datetime,timedelta
from app.helpers.redis_client import redis_client
from app.helpers.helper import generate_otp
import os,logging
from datetime import datetime,timedelta,timezone
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=['bcrypt'],deprecated="auto")

logging.basicConfig(
    level=logging.INFO,
    
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# hashing the password and then verifies the hashed password stored and the one that comes in 
# also retrives stored hashed_password

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)


def get_password_hash(password:str) -> str:
    return pwd_context.hash(password)


# hashing otp before storing it  and compare stored otp with what is being passed 
def hash_otp(otp: str):
    return pwd_context.hash(otp)

def verify_otp(raw_otp: str, stored_hash: str):
    try:
        return pwd_context.verify(raw_otp, stored_hash)
    except Exception:
        return False


# Generate access_token to user after user has been verified and set the expiry time for said token

def create_access_token(data: dict, expires_delta: timedelta = None):
    expire_seconds = expires_delta or timedelta(seconds=int(os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS", "900")))
    expire = datetime.now(timezone.utc) + expire_seconds

    payload = {
        "sub": data["email"],
        "user": {
            "id": data["id"],
            "name": data["name"],
            "email": data["email"],
            "role": data["role"]
        },
        "exp": expire
    }

    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    # Save in Redis
    redis_client.setex(f"access_token:{data['uid']}", int(expire_seconds.total_seconds()), encoded_jwt)

    return encoded_jwt
    
    
# Generate otp 
def generate_login_otp(data):
    try:
        otp = generate_otp()
        key = f"login_otp:{data.uid}"
        redis_client.setex(key, int(os.getenv("OTP_TOKEN_EXPIRE_SECONDS")), otp)   
        logging.info(f"LOGIN OTP GENERATED FOR {data.email} >>> {otp}")
        print(otp)
        return otp
    except Exception as e:
        logging.error(f"ERROR GENERATING LOGIN OTP {str(e)}")
        return False
    
def retrieve_login_otp(uid:str):
    try:
        key=f"login_otp:{uid}"
        otp=redis_client.get(key)
        
        if otp is None:
            logging.warning(f"No OTP found for UID: {uid}")
            return None 
        otp = otp.decode("utf-8")
        return otp
    except Exception as e:
        logging.warning(f"ERROR RETRIEVING LOGIN OTP {str(e)}")
        return None
    
def generate_forgot_password_otp(data):
    try:
        otp = generate_otp()
        expire_seconds = int(os.getenv("OTP_TOKEN_EXPIRE_SECONDs", "300"))  # fallback to 5 mins
        key = f"forgot_password_otp:{data.uid}"
        redis_client.setex(key, timedelta(seconds=expire_seconds), otp)
        logging.info(f"FORGOT PASSWORD OTP GENERATED FOR {data.email}")
        return otp
    except Exception as e:
        logging.warning(f"ERROR GENERATING FORGOT PASS OTP {str(e)}")
        return False

def retrive_forgot_otp(uid:str):
    try:
        key=f"forgot_password_otp:{uid}" 
        otp=redis_client.get(key)
        
        if otp is None:
            logging.warning(f"NO OTP FOUND FOR UID:{uid}")
            return None
        
        otp =otp.decode("utf-8")
        return otp
    except Exception as e:
        logging.warning(f"ERROR RETRIEVING FORGOT PASSWORD OTP {str(e)}")
        return None
    
    
def delete_redis_value(key):
    try:
        redis_client.delete(key)
    except Exception as e:
        logging.error(f"ERROR DELETING REDIS VALUE {str(e)}")        
                  
    
    