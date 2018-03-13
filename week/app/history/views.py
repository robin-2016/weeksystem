#!/usr/bin/env python
# -*-coding:utf-8 -*-

from flask import render_template,request,jsonify,redirect,url_for,flash,session
from flask_login import login_required,current_user
from ..history import history
from ..func import huizong,getlastweektime,getweektime
from .forms import HistoryForm

data = {}

@history.route("/historys",methods=['GET','POST'])
@login_required
def historys():
	global data
	nweek = str(getweektime())[4:]
	myform = HistoryForm()
	if data.get(current_user.name) == None:
		yearweek = getlastweektime()
		myform.week.data = int(str(yearweek)[4:])
	else:
		yearweek = data[current_user.name]
		myform.week.data = int(str(data[current_user.name])[4:])
	hweek = myform.week.data
	hdata = huizong(str(current_user.name),yearweek)
	if request.method == "POST":
		data[current_user.name] = int(request.form['year'] + request.form['week'])
		return redirect(url_for("history.historys"))
	return render_template("history.html",form=myform,data=hdata,nweek=nweek,hweek=hweek)