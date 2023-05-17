import random, string
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def randomstr(n: int):
    return "".join(random.choices(string.ascii_letters + string.digits, k=n))


def get_password_hashed(password: str, salt: str):
    return pwd_context.hash(salt + password)


def check_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
