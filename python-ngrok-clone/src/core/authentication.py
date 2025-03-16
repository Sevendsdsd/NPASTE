from datetime import datetime, timedelta
import jwt
import hashlib

SECRET_KEY = "your_secret_key"  # Replace with a secure key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REVOGED_TOKENS = set()  # Store revoked tokens in memory (can be replaced with a database)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if token in REVOGED_TOKENS:
            return None
        return payload
    except jwt.PyJWTError:
        return None

def revoke_token(token: str):
    """Revoke a token by adding it to the revoked tokens set."""
    REVOGED_TOKENS.add(token)

def is_token_valid(token: str):
    return verify_token(token) is not None

def generate_api_key(user_id: str):
    """Generate a unique API key for a user."""
    raw_key = f"{user_id}:{datetime.utcnow()}:{SECRET_KEY}"
    return hashlib.sha256(raw_key.encode()).hexdigest()

def validate_api_key(api_key: str, allowed_keys: set):
    """Validate if the provided API key is in the allowed keys."""
    return api_key in allowed_keys