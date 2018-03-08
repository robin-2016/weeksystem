#!/usr/bin/env python
#-*-coding=utf-8-*-
import time,datetime,os
from collections import Counter
from flask import render_template,request,redirect,url_for,flash
from flask_login import login_required
from .. import db
from ..tongji import tongji
from ..models import Users,Role,Groups,Newdata
from .forms import TongjiForm,YuetongjiForm
from ..func import getlastweektime

wday = 5
yweek = getlastweektime()
mday = 28

def getweeks():
	mlast = datetime.date.today() - datetime.timedelta(days=datetime.datetime.now().day)
	mfirst = mlast - datetime.timedelta(days=mlast.day - 1)
	# print mfirst
	# print mlast
	# print mlast.strftime("%W")
	# print mlast.strftime("%w")
	# print type(mlast.strftime("%w"))
	# print mfirst.strftime("%W")
	# print mfirst.strftime("%w")
	#	print mfirst-datetime.timedelta(days=-1)
	#	print (mfirst-datetime.timedelta(days=-1)).strftime("%W")
	#	print mfirst-datetime.timedelta(days=1)
	#	print (mfirst-datetime.timedelta(days=1)).strftime("%W")
	if int(mfirst.strftime("%w")) <= 2:
		fweek = int(mfirst.strftime("%W"))
	else:
		fweek = int(mfirst.strftime("%W")) + 1
	if int(mlast.strftime("%w")) >= 2:
		lweek = int(mlast.strftime("%W"))
	else:
		lweek = int(mlast.strftime("%W")) - 1
#	print fweek,lweek
	return [fweek,lweek]

@tongji.route('/tongji',methods=['GET','POST'])
@login_required
def tongji01():
	myform = TongjiForm()
	myform.weekday.data = 5
	if myform.validate_on_submit():
		if myform.weekday.data != None or myform.weekday.data != 5:
			global wday
			global yweek
			wday = int(request.form['weekday'])
			yweek = request.form['yweek']
		return redirect(url_for('tongji.compute'))
	return render_template('form.html',form=myform)

#get monday time
#def tmonday():
#	week = datetime.datetime.now().weekday()
#	return 
	

@tongji.route('/result')
@login_required
def compute():
	uptime = []
	zhoubao = []
	wtime = []
	if yweek == getlastweektime():
		tweek = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
		yweeklabel=u'上周'
	elif yweek == (int(time.strftime("%W"))-2):
		tweek = datetime.date.today() - datetime.timedelta(days=(datetime.date.today().weekday()+7))
		yweeklabel=u'上上周'
	else:
		tweek = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
		yweeklabel=u'上周'
#	print yweek
	montime=(datetime.datetime.strptime(str(tweek),'%Y-%m-%d')).replace(hour=9,minute=30,second=00)
	users = db.session.query(Users.name,Groups.name).outerjoin(Groups,Users.groups_id==Groups.id).all()
	for i in users:
		# data = db.session.query(Daydata.worktime,Daydata.time).filter_by(user=str(i[0])).filter_by(yearweek=yweek).order_by(Daydata.week.desc()).limit(7).all()
		data = db.session.query(Newdata.worktime,Newdata.time,Newdata.week).filter_by(user=str(i[0])).filter_by(
			yearweek=yweek).all()
		if data != []:
			# 统计提交时间
			tlist = []
			for b in data:
				tlist.append(b.time)
			maxtlist = max(tlist)
			if maxtlist > montime:
				uptime.append((i[1],i[0],maxtlist))
			# 统计工作量
			wk = 0
			for a in data:
				wk = wk + float(a.worktime)
			if wk < wday * 8:
				wtime.append((i[1], i[0], (wday * 8 - wk)))
			# 统计周报天数
			tianshu = set([])
			for c in data:
				tianshu.add(c.week)
				tianshu = tianshu
			week_tianshu = len(tianshu)
			if week_tianshu < wday:
				zhoubao.append((i[1],i[0],wday-week_tianshu))
		else:
			uptime.append((i[1],i[0],''))
			wtime.append((i[1], i[0], (wday * 8)))
			zhoubao.append((i[1], i[0],wday))
	#统计已完成人员
	wancheng = []
	renyuan = []
	for m in uptime:
		renyuan.append(m[1])
	for n in zhoubao:
		renyuan.append(n[1])
	for o in wtime:
		renyuan.append(o[1])
	# print renyuan
	for t in users:
		# print t[0]
		if t[0] not in renyuan:
			wancheng.append(t[0])
	return render_template('result.html',uptime=sorted(uptime),zhoubao=sorted(zhoubao),wtime=sorted(wtime),yweeklabel=yweeklabel,wancheng=wancheng)

@tongji.route('/yuetongji',methods=['GET','POST'])
@login_required
def tongji02():
	weeks = getweeks()
	fweek = weeks[0]
	lweek = weeks[1]
	myform = YuetongjiForm()
	myform.monthday.data = 28
	if request.method == "POST":
		if myform.validate_on_submit() and int(request.form['monthday']) != None and int(request.form['monthday']) <= 31:
			global mday
			mday = int(request.form['monthday'])
			return redirect(url_for("tongji.hebing"))
		else:
			flash(u"月工作天数错误！")
			# return render_template("yuetongji.html", form=myform, fweek=fweek, lweek=lweek, nweek=time.strftime("%W"))
	return render_template("yuetongji.html",form=myform,fweek=fweek,lweek=lweek,nweek=time.strftime("%W"))

@tongji.route('/yueresult')
@login_required
def hebing():
	zhoubao = []
	wtime = []
	weeks = getweeks()
	fweek = weeks[0]
	lweek = weeks[1]
	users = db.session.query(Users.name, Groups.name).outerjoin(Groups, Users.groups_id == Groups.id).all()
	for i in users:
		data = db.session.query(Newdata.worktime,Newdata.week,Newdata.yearweek).filter_by(user=str(i[0])).filter(Newdata.yearweek>=fweek).filter(Newdata.yearweek<=lweek).all()
		# print(data)
		if data != []:
			# 统计工作量
			wk = 0
			for a in data:
				wk = wk + float(a.worktime)
			if wk < mday * 8:
				wtime.append((i[1], i[0], (mday * 8 - wk)))
			# 统计周报天数
			tianshu = set([])
			for c in data:
				tianshu.add(str(c.yearweek)+str(c.week))
				tianshu = tianshu
			# print(tianshu)
			month_tianshu = len(tianshu)
			if month_tianshu < mday:
				zhoubao.append((i[1], i[0], mday - month_tianshu))
		else:
			wtime.append((i[1], i[0], (mday * 8)))
			zhoubao.append((i[1], i[0], mday))
	# 统计已完成人员
	wancheng = []
	renyuan = []
	for n in zhoubao:
		renyuan.append(n[1])
	for o in wtime:
		renyuan.append(o[1])
	for t in users:
		if t[0] not in renyuan:
			wancheng.append(t[0])
	return render_template('yueresult.html',zhoubao=sorted(zhoubao),wtime=sorted(wtime),wancheng=wancheng,fweek=fweek,lweek=lweek,nweek=time.strftime("%W"))