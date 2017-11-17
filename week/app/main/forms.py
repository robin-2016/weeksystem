#/bin/python
#-*-coding=utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time,datetime
from flask_wtf import FlaskForm
from wtforms import validators,SubmitField,StringField,SelectField,ValidationError,TextAreaField
from ..models import Groups,Users

class JcForm(FlaskForm):
	something0 = TextAreaField("*工作内容1：", [validators.data_required(message="工作内容1为空！"),
	                                       validators.Length(1, 400, message="工作内容1长度超出400限制！")])
	worktime0 = StringField("当日工作量1（H）：（注意：填写数字即可）",
	                        [validators.Optional(), validators.regexp('^\d{1,2}$', 0, '工作量1只能使用两位以内数字')])
	completed0 = StringField("周完成情况1（%）：", [validators.Optional(), validators.regexp('^\d{1,3}$', 0, '周完成情况1只能使用三位以内数字')])
	something1 = TextAreaField("工作内容2：", [validators.Length(0, 400, message="工作内容2长度超出400限制！")])
	worktime1 = StringField("当日工作量2:", [validators.Optional(), validators.regexp('^\d{1,2}$', 0, '工作量2只能使用两位以内数字')])
	completed1 = StringField("周完成情况2：", [validators.Optional(), validators.regexp('^\d{1,3}$', 0, '周完成情况2只能使用三位以内数字')])
	something2 = TextAreaField("工作内容3：", [validators.Length(0, 400, message="工作内容3长度超出400限制！")])
	worktime2 = StringField("当日工作量3:", [validators.Optional(), validators.regexp('^\d{1,2}$', 0, '工作量3只能使用两位以内数字')])
	completed2 = StringField("周完成情况3：", [validators.Optional(), validators.regexp('^\d{1,3}$', 0, '周完成情况3只能使用三位以内数字')])
	something3 = TextAreaField("工作内容4：", [validators.Length(0, 400, message="工作内容4长度超出400限制！")])
	worktime3 = StringField("当日工作量4:", [validators.Optional(), validators.regexp('^\d{1,2}$', 0, '工作量4只能使用两位以内数字')])
	completed3 = StringField("周完成情况4：", [validators.Optional(), validators.regexp('^\d{1,3}$', 0, '周完成情况4只能使用三位以内数字')])
	more0 = TextAreaField("更多：", [validators.Length(0, 400, message="更多内容长度超出400限制！")])
	more1 = StringField("更多当日工作量：", [validators.Optional(), validators.regexp('^\d{1,2}$', 0, '更多工作量只能使用两位以内数字')])
	more2 = StringField("更多周完成情况：", [validators.Optional(), validators.regexp('^\d{1,3}$', 0, '更多周完成情况只能使用三位以内数字')])
	submit = SubmitField("提交")

class InsertForm(JcForm):
	yearweek = SelectField("*周数：",coerce=int)
	week = SelectField("*星期：",coerce=int,default=((datetime.datetime.now()).weekday()))
#	project = SelectField("*项目：",coerce=int,default=projectid.groups_id)
	project = SelectField("*项目：",coerce=int)

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

class UpdateForm(JcForm):
	pass