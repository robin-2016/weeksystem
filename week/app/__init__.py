#/bin/python
#-*-coding=utf-8-*-

from flask import Flask,render_template
from flask_bootstrap import Bootstrap,WebCDN,ConditionalCDN,BOOTSTRAP_VERSION,JQUERY_VERSION,HTML5SHIV_VERSION,RESPONDJS_VERSION
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login.denglu'

def creat_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
#	print config[config_name]
	config[config_name].init_app(app)
	bootstrap.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)
	from .login import login as login_blueprint
	app.register_blueprint(login_blueprint)
	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)
	from .muser import muser as muser_blueprint
	app.register_blueprint(muser_blueprint,url_prefix='/muser')
	from .zhoubaos import zhoubaos as zhoubaos_blueprint
	app.register_blueprint(zhoubaos_blueprint,url_prefix='/zhoubaos')
	from .tongji import tongji as tongji_blueprint
	app.register_blueprint(tongji_blueprint)
	return app
