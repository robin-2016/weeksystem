#/bin/python
#-*-coding=utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask_wtf import FlaskForm
from wtforms import SelectField,StringField,SubmitField
from ..models import Groups,Role

class MuserForm(FlaskForm):
	name=StringField("用户名：")
	role=SelectField("角色：",coerce=int)
	groups=SelectField("分组：",coerce=int)
	submit=SubmitField("提交")
	
	def __init__(self,*args,**kwargs):
		super(MuserForm,self).__init__(*args,**kwargs)
		self.groups.choices = [(groups.id,groups.name)
                               for groups in Groups.query.order_by(Groups.name).all()]
		self.role.choices = [(role.id,role.name)
                               for role in Role.query.order_by(Role.name).all()]
#		dvalues=(0,"无")
#		self.groups.choices.append(dvalues)
#		self.role.choices.append(dvalues)
