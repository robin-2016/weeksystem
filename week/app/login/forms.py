#/bin/python
#-*-coding=utf-8-*-
from flask_wtf import FlaskForm
from wtforms import validators,SubmitField,StringField,PasswordField,BooleanField,SelectField,ValidationError
from wtforms.validators import data_required,Length,Regexp,EqualTo
from ..models import Users,Role,Groups

class LoginForm(FlaskForm):
	username = StringField(u"用户名：",[validators.data_required()])
	passwd = PasswordField(u"密码：",[validators.data_required()])
	remember_me = BooleanField(u"记住我")
	submit = SubmitField(u"登录")

class UseraddForm(FlaskForm):
	username = StringField(u"用户名：")
	passwd = PasswordField(u"密码：")
	passwd2 = PasswordField(u"确认密码：")
	groups = SelectField(u"分组", coerce=int)
	submit = SubmitField(u'注册')
	
	def __init__(self,*args,**kwargs):
		super(UseraddForm,self).__init__(*args,**kwargs)
		self.groups.choices = [(groups.id,groups.name)
					for groups in Groups.query.order_by(Groups.name).all()]

class ChangepwForm(FlaskForm):
	passwdold = PasswordField(u"旧密码：",[validators.data_required()])
	passwd = PasswordField(u"新密码：",validators=[data_required(),EqualTo('passwd2',message=u'两次密码不相同！')])
	passwd2 = PasswordField(u"确认密码：",validators=[data_required()])
	submit = SubmitField(u'更改密码')
