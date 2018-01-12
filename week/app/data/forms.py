#/bin/python
#-*-coding=utf-8-*-

from flask_wtf import FlaskForm
from wtforms import validators,SubmitField,StringField,SelectField,TextAreaField
from ..models import Groups

class DataForm(FlaskForm):
	project = SelectField(u"*项目：", coerce=int)
	week = SelectField(u"*星期：",
	                    choices=[(0,u'星期一'),(1,u'星期二'),(2,u'星期三'),(3,u'星期四'),(4,u'星期五'),(5,u'星期六'),(6,u'星期日')])
	something = TextAreaField(u"*工作内容：", [validators.data_required(message=u"工作内容为空！"),
	                                       validators.Length(1, 400, message=u"工作内容长度超出400限制！")])
	worktime = StringField(u"当日工作量（/小时）：",
	                        [validators.Optional(), validators.regexp('^((([1-9])|(1[0-9])|(2[0-4]))|((([0-9])|(1[0-9])|(2[0-3])).\d))$', 0, u'工作量超出1-24范围')])
	completed = StringField(u"周完成情况（/%）：", [validators.Optional(), validators.regexp('^100$|^(\d|[1-9]\d)$', 0, u'周完成情况超出0-100范围')])

	def __init__(self, *args, **kwargs):
		super(DataForm, self).__init__(*args, **kwargs)
		self.project.choices = [(project.id, project.name)
		                        for project in Groups.query.order_by(Groups.name).all()]


