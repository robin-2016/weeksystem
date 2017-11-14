class Config:
	SECRET_KEY = 'test321'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	BOOTSTRAP_SARVE_LOCAL = True
	FLASKY_POSTS_PER_PAGE = 20

	@staticmethod
	def init_app(app):
		pass
class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = "mysql://week:asd@192.168.1.169:3306/week"
class ProductionConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = "mysql://week:asd@192.168.1.169:3306/week"
config = {
	'development': DevelopmentConfig,
	'production': ProductionConfig,
	
	'default': DevelopmentConfig	
}
