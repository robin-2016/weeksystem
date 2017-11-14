import os
from flask_script import Manager,Server
from app import creat_app,db
from flask_migrate import Migrate,MigrateCommand


app = creat_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
manager.add_command("runserver",Server(host="192.168.1.169"))
migrate = Migrate(app,db)
manager.add_command("db",MigrateCommand)

if __name__ == '__main__':
	manager.run()
