# manage.py

# Script that manages database running and migrations
import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db

app.config.from_object(os.environ.get('APP_SETTINGS'))
manager = Manager(app)
migrate = Migrate(app, db)

@manager.command
def create(default_data = True, sample_data = False):
    # 'Creates the database tables'
    db.create_all()

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()