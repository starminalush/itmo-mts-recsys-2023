import json
from os import getenv

import jwt
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET: str = getenv("JWT_SECRET")
JWT_ALGORITHM: list[str] = json.loads(getenv("JWT_ALGORITHM"))


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
        return decoded_token
    except jwt.InvalidSignatureError:
        return {}


def token_response(token: str):
    return {"access_token": token}
