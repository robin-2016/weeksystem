from app import db,login_manager
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import UserMixin

class Users(UserMixin,db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer,primary_key=True)
        name = db.Column(db.String(50),unique=True)
        passwd = db.Column(db.String(100))
        role_id = db.Column(db.Integer)
        groups_id = db.Column(db.Integer)
        uptime = db.Column(db.DateTime)

        @property
        def password_hash(self):
                raise AttributeError('Password is not a readable attribute!')
        @password_hash.setter
        def password_hash(self,password):
                self.passwd = generate_password_hash(password)
        def verify_password(self,password):
                return check_password_hash(self.passwd,password)
	@login_manager.user_loader
	def load_user(user_id):
		return Users.query.get(int(user_id))

class Role(db.Model):
	__tablename__='role'
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(20))

	@staticmethod
	def insert_role():
		for r in ["admin","user","renli","nothing"]:
			role = Role.query.filter_by(name=r).first()
			if role is None:
				role = Role(name=r)
				db.session.add(role)
		db.session.commit()

class Groups(db.Model):
	__tablename__='groups'
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(50))

	@staticmethod
	def insert_groups():
		groups = Groups.query.filter_by(name="nothing").first()
		if groups is None:
			groups = Groups(name="nothing")
			db.session.add(groups)
			db.session.commit()

class Daydata(db.Model):
	__tablename__='daydata'
	id = db.Column(db.Integer,primary_key=True)
	user = db.Column(db.String(100))
	project_id = db.Column(db.Integer)
	worktime = db.Column(db.Float)
	completed = db.Column(db.Integer)
	something0 = db.Column(db.Text)
	worktime0 = db.Column(db.String(5))
	completed0 = db.Column(db.String(5))
	something1 = db.Column(db.Text)
	worktime1 = db.Column(db.String(5))
	completed1 = db.Column(db.String(5))
	something2 = db.Column(db.Text)
	worktime2 = db.Column(db.String(5))
	completed2 = db.Column(db.String(5))
	something3 = db.Column(db.Text)
	worktime3 = db.Column(db.String(5))
	completed3 = db.Column(db.String(5))
	more0 = db.Column(db.Text)
	more1 = db.Column(db.String(5))
	more2 = db.Column(db.String(5))
	time = db.Column(db.DateTime)
	yearweek = db.Column(db.Integer)
	week = db.Column(db.Integer)
