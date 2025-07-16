# app/utils/validators.py
import re, phonenumbers  
  

def validate_password(v: str) -> str:
    if len(v) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if not re.search(r"[A-Z]", v):
        raise ValueError("Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", v):
        raise ValueError("Password must contain at least one lowercase letter")
    if not re.search(r"[0-9]", v):
        raise ValueError("Password must contain at least one number")
    if not re.search(r"[\W_]", v):
        raise ValueError("Password must contain at least one special character")
    return v



def validate_kenyan_phone_number(phone_number: str) -> str:
    try:
        parsed = phonenumbers.parse(phone_number, "KE")  # Kenya
        if not phonenumbers.is_valid_number(parsed):
            raise ValueError("Invalid phone number format")

        if not phone_number.startswith("254") or len(phone_number) != 12:
            raise ValueError("Phone number must start with '254' and be 12 digits long")

    except Exception as e:
        raise ValueError("Invalid phone number format")
    
    return phone_number