import jwt
from hashlib import sha256
from src.config import config
from datetime import datetime, timedelta
from fastapi import status, HTTPException


class JWTHandler:
    @staticmethod
    def encode(payload: dict) -> str:
        expire = datetime.utcnow() + timedelta(
            minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        payload.update({"exp": expire})
        return jwt.encode(
            payload, config.AUTHORIZATION_SECRET_KEY, algorithm=config.ALGORITHM
        )
    
    @staticmethod
    def decode(token: str) -> dict:
        try:
            return jwt.decode(
                token, config.AUTHORIZATION_SECRET_KEY, algorithms=[config.ALGORITHM]
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )


class SignatureHandler:
    @staticmethod
    def _format_payload(payload: dict) -> str:
        return "{}{}{}{}{}".format(
            payload["account_id"],
            payload["amount"],
            payload["transaction_id"],
            payload["user_id"],
            config.TRANSACTION_SECRET_KEY
        )
    
    @staticmethod
    def hash_signature(payload: dict) -> str:
        signature = SignatureHandler._format_payload(payload)
        return sha256(signature.encode("utf-8")).hexdigest()
    
    @staticmethod
    def verify_signature(transaction_data: dict) -> None:
        if SignatureHandler.hash_signature(transaction_data) != transaction_data["signature"]:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                detail="Signature verification failed"
            )














