import jwt
import os
from dotenv import load_dotenv

load_dotenv()

PUBLIC_KEY = os.environ.get("PUBLIC_KEY")
PRIVATE_KEY = os.environ.get("PRIVATE_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


def create_access_token(data: dict):
    to_encode = data.copy()

    encoded_jwt = jwt.encode(to_encode, PRIVATE_KEY, algorithm=ALGORITHM)

    return encoded_jwt
