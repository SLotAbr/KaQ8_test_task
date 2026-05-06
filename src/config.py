from pydantic.v1 import BaseSettings


class Config(BaseSettings):
    DATABASE_URL: str
    TEST_DATABASE_URL: str
    
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str
    TEST_USER_EMAIL: str
    TEST_USER_PASSWORD: str
    
    AUTHORIZATION_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 5
    
    TRANSACTION_SECRET_KEY: str
    
    class Config:
        env_file = ".env.example"


config: Config = Config()

