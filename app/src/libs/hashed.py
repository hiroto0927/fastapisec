import random, string
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def randomstr(n:int):
   return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

def get_password_hashed(password:str,salt:str):
    return pwd_context.hash(salt+password)

def check_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)