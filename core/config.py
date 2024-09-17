import os
# from dotenv import load_dotenv

# load_dotenv()


class Settings:
    DB_USER: str = os.getenv("POSTGRES_USER", "")
    DB_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
    DB_HOST: str = os.getenv("POSTGRES_HOST", "")
    DB_PORT: str = os.getenv("POSTGRES_PORT", "")
    DB_NAME: str = os.getenv("POSTGRES_DB", "")

    DATABASE_URL: str = f"postgresql+asyncpg://{DB_USER}:{
        DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


settings = Settings()
