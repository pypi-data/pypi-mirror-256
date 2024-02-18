import os

import jwt

import datetime

from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


JWT_USER = os.getenv("JWT_USER")
JWT_PASSWORD = os.getenv("JWT_PASSWORD")
JWT_SECRET = os.getenv("SECRET_JWT_API")

class JWT():
    security = HTTPBearer()
    secret = JWT_SECRET
    user = JWT_USER
    password = JWT_PASSWORD

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload["user"]

        except jwt.ExpiredSignatureError as e:
            raise HTTPException(status_code=401, detail="Token Expirado") from e
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail="Token Invalido") from e

    def decode_token_all(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            user_types = ["user", "api_client", "admin"]
            if any(user_type in payload for user_type in user_types):
                payload["user_type"] = [user_type for user_type in user_types if user_type in payload][0]
                return payload
            raise ValueError("Invalid user_type")
        except jwt.ExpiredSignatureError as e:
            raise HTTPException(status_code=401, detail="Token Expirado") from e
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail="Token Invalido") from e

    def decode_token_user(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            user_types = ["user"]
            if any(user_type in payload for user_type in user_types):
                payload["user_type"] = [user_type for user_type in user_types if user_type in payload][0]
                return payload
            raise ValueError("Invalid user_type")
        except jwt.ExpiredSignatureError as e:
            raise HTTPException(status_code=401, detail="Token Expirado") from e
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail="Token Invalido") from e

    def decode_token_user_api_client(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            user_types = ["user", "api_client"]
            if any(user_type in payload for user_type in user_types):
                payload["user_type"] = [user_type for user_type in user_types if user_type in payload][0]
                return payload
            raise ValueError("Invalid user_type")
        except jwt.ExpiredSignatureError as e:
            raise HTTPException(status_code=401, detail="Token Expirado") from e
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail="Token Invalido") from e

    def decode_token_admin(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            user_types = ["admin"]
            if any(user_type in payload for user_type in user_types):
                payload["user_type"] = [user_type for user_type in user_types if user_type in payload][0]
                return payload
            raise ValueError("Invalid user_type")
        except jwt.ExpiredSignatureError as e:
            raise HTTPException(status_code=401, detail="Token Expirado") from e
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail="Token Invalido") from e

    def auth_wrapper(
        self,
        auth: HTTPAuthorizationCredentials = Security(security)
    ):
        return self.decode_token(auth.credentials)

    def auth_user_api_client(
        self,
        auth: HTTPAuthorizationCredentials = Security(security)
    ):
        return self.decode_token_user_api_client(auth.credentials)

    def auth_admin(
        self,
        auth: HTTPAuthorizationCredentials = Security(security)
    ):
        return self.decode_token_admin(auth.credentials)

    def auth_all(
        self,
        auth: HTTPAuthorizationCredentials = Security(security)
    ):
        return self.decode_token_all(auth.credentials)


def create_access_token(exp_time):
    context = {
        "user": JWT_USER,
        "password": JWT_PASSWORD,
        "exp": exp_time + datetime.timedelta(minutes=5)
    }

    return jwt.encode(context, JWT_SECRET, algorithm="HS256")


def create_any_access_token(
    context: dict = {},
    secret:str =""
):
    return jwt.encode(context, secret, algorithm="HS256")