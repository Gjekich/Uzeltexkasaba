import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME = "UzeltexKasaba"
    PROJECT_VERSION = "1.0.0"

    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
    )


settings = Settings()