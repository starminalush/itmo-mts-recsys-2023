import time
from os import getenv

import jwt

JWT_SECRET = getenv("JWT_SECRET")
JWT_ALGORITHM = getenv("JWT_ALGORITHM")


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}


def token_response(token: str):
    return {"access_token": token}


def signJWT(user_id: str) -> dict[str, str]:
    payload = {"user_id": user_id, "expires": time.time() + 86400}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    print(token)
    return token_response(token)
