class Config:

    SECRET_KEY = "your_secret_key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"

    JWT_SECRET_KEY = "jwt_secret_key"

    JWT_ACCESS_TOKEN_EXPIRES = 36000

    # redis config
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = "redis://localhost:6379/3"
    CACHE_DEFAULT_TIMEOUT = 300
