import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from settings import ENV_NAME
from src.app import create_app, db
from src.models.TodoModel import *
from src.models.UserModel import *


app = create_app(ENV_NAME)
print('Hi darling :) ')
migrate = Migrate(app=app, db=db)

manager = Manager(app=app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
