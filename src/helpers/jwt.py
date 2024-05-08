import jwt
from src.conf.environment import value


def verify_token(token: str) -> dict:
    return jwt.decode(token, value.get('SECRET'), algorithms=['HS256'])
