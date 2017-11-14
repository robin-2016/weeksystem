#/bin/python
#-*-coding=utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time
from flask_wtf import FlaskForm
from wtforms import IntegerField,validators,SubmitField,SelectField

class TongjiForm(FlaskForm):
	yweek = SelectField("*周数：",coerce=int)
	weekday = IntegerField("*上周天数（如果不是5天需修改）：")
	submit = SubmitField("开始统计")

	def __init__(self,*args,**kwargs):
                super(TongjiForm,self).__init__(*args,**kwargs)
                yweekid = int(time.strftime("%W"))
		self.yweek.choices = [((yweekid-1),'上周'),((yweekid-2),'上上周')]
