#/bin/python
#-*-coding=utf-8-*-
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
import time
from flask_wtf import FlaskForm
from wtforms import IntegerField,validators,SubmitField,SelectField
from ..func import getlastweektime

class TongjiForm(FlaskForm):
	yweek = SelectField(u"*周数：",coerce=int)
	weekday = IntegerField(u"*上周工作天数（如果不是5天需修改）：")
	submit = SubmitField(u"开始统计")

	def __init__(self,*args,**kwargs):
		super(TongjiForm,self).__init__(*args,**kwargs)
		yweekid = getlastweektime()
		self.yweek.choices = [((yweekid),u'上周'),((yweekid-1),u'上上周')]

class YuetongjiForm(FlaskForm):
	monthday = IntegerField(u"*上月工作天数（如果不是需修改）：")
	submit = SubmitField(u"开始统计")