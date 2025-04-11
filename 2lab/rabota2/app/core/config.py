import os
class Settings:
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "sqlite:///./test.db")
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

settings = Settings()
