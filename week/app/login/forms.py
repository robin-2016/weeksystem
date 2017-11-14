#/bin/python
#-*-coding=utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask_wtf import FlaskForm
from wtforms import TextField,validators,SubmitField,StringField,PasswordField,BooleanField,SelectField,IntegerField,ValidationError
from wtforms.validators import Required,Length,Regexp,EqualTo
from ..models import Users,Role,Groups

class LoginForm(FlaskForm):
	username = StringField("用户名：",[validators.Required()])
	passwd = PasswordField("密码：",[validators.Required()])
	remember_me = BooleanField("记住我")
	submit = SubmitField("登录")

class UseraddForm(FlaskForm):
	username = StringField("用户名：",validators=[Required(),Length(1,100),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'只能使用字母、数字、下划线和点号！')])
	passwd = PasswordField("密码：",validators=[Required(),EqualTo('passwd2',message='两次密码不相同！')])
	passwd2 = PasswordField("确认密码：",validators=[Required()])
#	role = SelectField("角色",coerce=int)
	groups = SelectField("分组",coerce=int)
	submit = SubmitField('新增用户')
	
	def __init__(self,*args,**kwargs):
		super(UseraddForm,self).__init__(*args,**kwargs)
#		self.role.choices = [(role.id,role.name)
#					for role in Role.query.order_by(Role.name).all()]
		self.groups.choices = [(groups.id,groups.name)
					for groups in Groups.query.order_by(Groups.name).all()]

	def validate_username(self,field):
		if Users.query.filter_by(name=field.data).first():
			raise ValidationError('用户名已经存在！')

class ChangepwForm(FlaskForm):
	passwdold = PasswordField("旧密码：",[validators.Required()])
	passwd = PasswordField("新密码：",validators=[Required(),EqualTo('passwd2',message='两次密码不相同！')])
	passwd2 = PasswordField("确认密码：",validators=[Required()])
	submit = SubmitField('更改密码')
