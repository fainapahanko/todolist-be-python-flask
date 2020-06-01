import os
from src.app import create_app
from settings import ENV_NAME, DATABASE_URL


if __name__ == '__main__':
    app = create_app(ENV_NAME)
    # app.config['SQLACHEMY_DATABASE_URI'] = DATABASE_URL
    app.run()
