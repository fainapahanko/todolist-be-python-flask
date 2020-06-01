from settings import JWT_SECRET_KEY, DATABASE_URL


class Development(object):
    """
    Development environment configuration
    """
    DEBUG = True
    TESTING = False
    JWT_SECRET_KEY = JWT_SECRET_KEY
    SQLALCHEMY_DATABASE_URI = DATABASE_URL


class Production(object):
    """
    Development environment configuration
    """
    DEBUG = False
    TESTING = False
    JWT_SECRET_KEY = JWT_SECRET_KEY
    SQLALCHEMY_DATABASE_URI = DATABASE_URL


app_config = {
    'development': Development,
    'production': Production
}
