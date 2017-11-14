#/bin/python
#-*-coding=utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time,datetime
from flask_wtf import FlaskForm
from wtforms import validators,SubmitField,StringField,SelectField,ValidationError,TextAreaField,FloatField,IntegerField
from ..models import Groups,Users
from flask_login import current_user
#from .. import db

#prodectid=db.session.query(Users.groups_id).filter_by(name=(str(current_user.name))).first()
#projectid=Users.query.filter_by(name=(str(current_user.name))).first()
dweek=(datetime.datetime.now()).weekday()
class InsertForm(FlaskForm):
	yearweek = SelectField("*周数：",coerce=int)
	week = SelectField("*星期：",coerce=int,default=dweek)
#	project = SelectField("*项目：",coerce=int,default=projectid.groups_id)
	project = SelectField("*项目：",coerce=int)
	something0 = TextAreaField("*工作内容1：",[validators.Required()])
	worktime0 = FloatField("当日工作量1（H）：（注意：填写数字即可）",[validators.Optional()])
	completed0 = IntegerField("周完成情况1（%）：",[validators.Optional()])
	something1 = TextAreaField("工作内容2：")
	worktime1 = FloatField("当日工作量2:",[validators.Optional()])
	completed1 = IntegerField("周完成情况2：",[validators.Optional()])
	something2 = TextAreaField("工作内容3：")
	worktime2 = FloatField("当日工作量3:",[validators.Optional()])
	completed2 = IntegerField("周完成情况3：",[validators.Optional()])
	something3 = TextAreaField("工作内容4：")
	worktime3 = FloatField("当日工作量4:",[validators.Optional()])
	completed3 = IntegerField("周完成情况4：",[validators.Optional()])
	more0 = TextAreaField("更多：")
	more1 = FloatField("更多当日工作量：",[validators.Optional()])
	more2 = IntegerField("更多周完成情况：",[validators.Optional()])
	submit = SubmitField("提交")
	

	def __init__(self,*args,**kwargs):
		super(InsertForm,self).__init__(*args,**kwargs)
		yweekid = int(time.strftime("%W"))
#		yweekstr = '本周第'+(time.strftime("%W"))+'周'
#		yweeklast = '上周第'+(str(yweekid-1))+'周'
		weekchoices = [(0,'星期一'),(1,'星期二'),(2,'星期三'),(3,'星期四'),(4,'星期五'),(5,'星期六'),(6,'星期日')]
		self.yearweek.choices = [(yweekid,'本周'),((yweekid-1),'上周')]
		self.week.choices = weekchoices
		self.project.choices = [(project.id,project.name)
				for project in Groups.query.order_by(Groups.name).all()]

class UpdateForm(FlaskForm):
	something0 = TextAreaField("*工作内容1：",[validators.Required()])
	worktime0 = FloatField("当日工作量1（H）：（注意：填写数字即可）",[validators.Optional()])
	completed0 = IntegerField("周完成情况1（%）：",[validators.Optional()])
	something1 = TextAreaField("工作内容2：")
	worktime1 = FloatField("当日工作量2:",[validators.Optional()])
	completed1 = IntegerField("周完成情况2：",[validators.Optional()])
	something2 = TextAreaField("工作内容3：")
	worktime2 = FloatField("当日工作量3:",[validators.Optional()])
	completed2 = IntegerField("周完成情况3：",[validators.Optional()])
	something3 = TextAreaField("工作内容4：")
	worktime3 = FloatField("当日工作量4:",[validators.Optional()])
	completed3 = IntegerField("周完成情况4：",[validators.Optional()])
	more0 = TextAreaField("更多：")
	more1 = FloatField("更多当日工作量：",[validators.Optional()])
	more2 = IntegerField("更多周完成情况：",[validators.Optional()])
	submit = SubmitField("提交")
