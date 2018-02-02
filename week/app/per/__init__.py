#!/usr/bin/env python
#-*-coding:utf-8-*-
from flask import session,flash,redirect,url_for
from flask_login import current_user
from ..models import Users
from functools import wraps

def isadmin(func):
	@wraps(func)
	def test1():
		if session['role'] == 'admin':
			func()
		else:
			flash(u"没有访问权限！")
			return redirect(url_for("main.index"))
	return test1

# def iscurrent_user_id(func):
# 	def test2():
# 		if

