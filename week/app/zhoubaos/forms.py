#/bin/python
#-*-coding=utf-8-*-
from flask_wtf import FlaskForm
from wtforms import StringField,validators,SubmitField,TextAreaField

class ScoreForm(FlaskForm):
	score = StringField(u"*评分（0-100分）：", [validators.regexp('^100$|^(\d|[1-9]\d)$', 0, '超出0-100范围')])
	comment = TextAreaField(u"评价（选填）：",[validators.Optional()])

class TijiaoForm(ScoreForm):
	submit = SubmitField(u"提交")