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
	# something1 = TextAreaField(u"工作内容2：", [validators.Length(0, 400, message=u"工作内容2长度超出400限制！")])
	# worktime1 = StringField(u"当日工作量2:", [validators.Optional(), validators.regexp('^((([1-9])|(1[0-9])|(2[0-4]))|((([0-9])|(1[0-9])|(2[0-3])).\d))$', 0, u'工作量2超出1-24范围')])
	# completed1 = StringField(u"周完成情况2：", [validators.Optional(), validators.regexp('^100$|^(\d|[1-9]\d)$', 0, u'周完成情况2超出0-100范围')])
	# something2 = TextAreaField(u"工作内容3：", [validators.Length(0, 400, message=u"工作内容3长度超出400限制！")])
	# worktime2 = StringField(u"当日工作量3:", [validators.Optional(), validators.regexp('^((([1-9])|(1[0-9])|(2[0-4]))|((([0-9])|(1[0-9])|(2[0-3])).\d))$', 0, u'工作量3超出1-24范围')])
	# completed2 = StringField(u"周完成情况3：", [validators.Optional(), validators.regexp('^100$|^(\d|[1-9]\d)$', 0, u'周完成情况3超出0-100范围')])
	# something3 = TextAreaField(u"工作内容4：", [validators.Length(0, 400, message=u"工作内容4长度超出400限制！")])
	# worktime3 = StringField(u"当日工作量4:", [validators.Optional(), validators.regexp('^((([1-9])|(1[0-9])|(2[0-4]))|((([0-9])|(1[0-9])|(2[0-3])).\d))$', 0, u'工作量4超出1-24范围')])
	# completed3 = StringField(u"周完成情况4：", [validators.Optional(), validators.regexp('^100$|^(\d|[1-9]\d)$', 0, u'周完成情况4超出0-100范围')])
	# more0 = TextAreaField(u"更多：", [validators.Length(0, 400, message=u"更多内容长度超出400限制！")])
	# more1 = StringField(u"更多当日工作量：", [validators.Optional(), validators.regexp('^((([1-9])|(1[0-9])|(2[0-4]))|((([0-9])|(1[0-9])|(2[0-3])).\d))$', 0, u'更多工作量超出1-24范围')])
	# more2 = StringField(u"更多周完成情况：", [validators.Optional(), validators.regexp('^100$|^(\d|[1-9]\d)$', 0, u'更多周完成情况超出0-100范围')])
	# submit = SubmitField(u"提交")
	
	def __init__(self, *args, **kwargs):
		super(DataForm, self).__init__(*args, **kwargs)
		self.project.choices = [(project.id, project.name)
		                        for project in Groups.query.order_by(Groups.name).all()]


