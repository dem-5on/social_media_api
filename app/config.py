from pydantic_settings import BaseSettings
from pathlib import Path

# Get the parent directory where .env is located
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expires_minutes: int

    model_config = {
        "env_file": str(BASE_DIR / ".env"),
        # "env_file_encoding": "utf-8",
        # "case_sensitive": False
    }

# Debug prints to verify paths
# print(f"Base directory: {BASE_DIR}")
# print(f"Expected .env path: {BASE_DIR / '.env'}")
# print(f".env exists: {(BASE_DIR / '.env').exists()}")

settings = Settings()