from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.core.config import SECRET_KEY, ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hash password
def get_password_hash(password: str) -> str:
    # Truncate ONLY plain password (bytes)
    password_bytes = password.encode("utf-8")[:72]
    return pwd_context.hash(password_bytes)


# Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password[:72], hashed_password)



# Create JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_reset_token(email: str):
    expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode = {"sub": email, "exp": expire}

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_reset_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except:
        return None