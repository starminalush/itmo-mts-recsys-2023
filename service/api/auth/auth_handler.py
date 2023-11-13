from os import getenv

import jwt
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = getenv("JWT_SECRET")
JWT_ALGORITHM = getenv("JWT_ALGORITHM")


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
        return decoded_token
    except jwt.InvalidSignatureError:
        return {}


def token_response(token: str):
    return {"access_token": token}


def sign_jwt(user_id: str) -> dict[str, str]:
    payload = {"user_id": user_id, "expires": None}  # Set expires to None for infinite token
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)
