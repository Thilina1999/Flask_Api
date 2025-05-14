import os
class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Should typically be False for better performance
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 1000,                   # Default number of connections
        'max_overflow': 500,                 # Max connections allowed beyond pool_size
        'pool_timeout': 300,                 # Seconds to wait for a connection
        'pool_recycle': 200,               # Recycle connections after 1 hour
        'pool_pre_ping': True              # Test connections for health before use
    }
    PROPAGATE_EXCEPTIONS = True            # Better error handling
class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEVELOPMENT_DATABASE_URL")
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")
class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("STAGING_DATABASE_URL")
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("PRODUCTION_DATABASE_URL")
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "staging": StagingConfig,
    "production": ProductionConfig
}