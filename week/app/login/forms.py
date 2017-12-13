#/bin/python
#-*-coding=utf-8-*-
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
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
	username = StringField(u"用户名：", validators=[data_required(), Length(1, 100)])
	# username = StringField(u"用户名：", validators=[data_required(), Length(1, 100),
	#                                             Regexp('^[\u4e00-\u9fa5]', 0,
	#                                                    u'只能使用字母、数字、下划线和汉字！')])
	passwd = PasswordField(u"密码：",validators=[data_required(),EqualTo('passwd2',message=u'两次密码不相同！')])
	passwd2 = PasswordField(u"确认密码：",validators=[data_required()])
#	role = SelectField("角色",coerce=int)
	groups = SelectField(u"分组",coerce=int)
	submit = SubmitField(u'新增用户')
	
	def __init__(self,*args,**kwargs):
		super(UseraddForm,self).__init__(*args,**kwargs)
#		self.role.choices = [(role.id,role.name)
#					for role in Role.query.order_by(Role.name).all()]
		self.groups.choices = [(groups.id,groups.name)
					for groups in Groups.query.order_by(Groups.name).all()]

	def validate_username(self,field):
		if Users.query.filter_by(name=field.data).first():
			raise ValidationError(u'用户名已经存在！')

class ChangepwForm(FlaskForm):
	passwdold = PasswordField(u"旧密码：",[validators.data_required()])
	passwd = PasswordField(u"新密码：",validators=[data_required(),EqualTo('passwd2',message=u'两次密码不相同！')])
	passwd2 = PasswordField(u"确认密码：",validators=[data_required()])
	submit = SubmitField(u'更改密码')
