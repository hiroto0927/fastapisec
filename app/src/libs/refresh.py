import jwt
import os
from dotenv import load_dotenv
from src.schemas.auth import RefreshDecoded

load_dotenv()

PUBLIC_KEY = os.environ.get("PUBLIC_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


def decoded_refresh_token(encoded_refresh: str) -> RefreshDecoded:
    decoded_refresh = jwt.decode(encoded_refresh, PUBLIC_KEY, algorithms=ALGORITHM)

    response = RefreshDecoded(
        sub=decoded_refresh["sub"],
        kid=decoded_refresh["kid"],
        iat=decoded_refresh["iat"],
        exp=decoded_refresh["exp"],
    )

    return response
