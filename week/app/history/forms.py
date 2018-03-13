#!/usr/bin/env python
# -*-coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import SubmitField,SelectField

class HistoryForm(FlaskForm):
	year = SelectField(u"年",coerce=int)
	week = SelectField(u"周",coerce=int)
	submit = SubmitField(u'查询')

	def __init__(self,*args,**kwargs):
		super(HistoryForm,self).__init__(*args,**kwargs)
		self.year.choices=[(2018,2018)]
		self.week.choices=[(nu,nu) for nu in range(1,53)]