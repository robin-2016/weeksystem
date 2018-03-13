#!/usr/bin/python
#-*-coding:utf-8 -*-
# from datetime import datetime
# import time
from ..main import main
from flask import render_template,request,redirect,url_for,flash
from flask_login import login_required,current_user
# from .. import db
# from ..models import Daydata,Groups,Users,Newdata
# from .forms import InsertForm,UpdateForm
from ..func import huizong,getweektime

@main.route('/main')
@login_required
def index():
	weekdata = huizong(str(current_user.name),getweektime())
	return render_template('main.html',data=weekdata)

# @main.route('/insert',methods = ['GET','POST'])
# @main.route('/lastinsert',methods = ['GET','POST'])
# @login_required
# def insert():
# 	myform = InsertForm()
# 	if request.path == '/insert':
# 		yweek = int(time.strftime("%W"))
# 	elif request.path == '/lastinsert':
# 		if int(time.strftime("%W")) == 1:
# 			yweek = 52
# 		else:
# 			yweek = int(time.strftime("%W")) - 1
# 	else:
# 		yweek = int(time.strftime("%W"))
# 	projectid=Users.query.filter_by(name=(str(current_user.name))).first()
# 	if request.method == 'GET':
# 		myform.project.data=projectid.groups_id
# 		myform.week.data=((datetime.now()).weekday())
# 	if request.method == 'POST':
# 		if myform.validate_on_submit():
# 			if Daydata.query.filter_by(user=str(current_user.name)).filter_by(yearweek=yweek).filter_by(week=request.form['week']).first() is None:
# 				wtime=0
# 				for i in [myform.worktime0.data,myform.worktime1.data,myform.worktime2.data,myform.worktime3.data,myform.more1.data]:
# 					if i != "":
# 						wtime=wtime+float(i)
# 				a=0
# 				c=0
# 				for b in [myform.completed0.data,myform.completed1.data,myform.completed2.data,myform.completed3.data,myform.more2.data]:
# 					if b !="":
# 						c=c+int(b)
# 						a=a+1
# 				if c == 0:
# 					com = c
# 				else:
# 					com=c/a
# 				dinsert = Daydata(user=str(current_user.name),
# 					yearweek=yweek,
# 					week=myform.week.data,
# 					project_id=myform.project.data,
# 					worktime=wtime,
# 					worktime0=myform.worktime0.data,
# 					worktime1=myform.worktime1.data,
# 					worktime2=myform.worktime2.data,
# 					worktime3=myform.worktime3.data,
# 					completed0=myform.completed0.data,
# 					completed1=myform.completed1.data,
# 					completed2=myform.completed2.data,
# 					completed3=myform.completed3.data,
# 					something0=myform.something0.data,
# 					something1=myform.something1.data,
# 					something2=myform.something2.data,
# 					something3=myform.something3.data,
# 					more0=myform.more0.data,
# 					more1=myform.more1.data,
# 					more2=myform.more2.data,
# 					completed=com,
# 					time=datetime.now())
# 				db.session.add(dinsert)
# 				db.session.commit()
# 			#flash("Insert Successful!")
# 				if int(time.strftime("%W")) == yweek:
# 					return redirect(url_for('main.index'))
# 				elif (int(time.strftime("%W"))-1) == yweek:
# 					return redirect(url_for('zhoubaos.zbdata',name=str(current_user.name)))
# 				elif int(time.strftime("%W")) == 1 and yweek == 52:
# 					return redirect(url_for('zhoubaos.zbdata', name=str(current_user.name)))
# 				else:
# 					return redirect(url_for('main.index'))
# 			else:
# 				flash(u'星期数据重复！请修改。')
# 				return render_template('insert.html',form=myform)
# 		else:
# 			# print myform.errors
# 			# print myform.errors.values()[0][0]
# 			flash(u'增加数据失败！'+myform.errors.values()[0][0])
# 			return render_template('insert.html',form=myform)
# 	return render_template('insert.html',form=myform)
#
# @main.route('/update/<id>',methods=['GET','POST'])
# @login_required
# def update(id):
# 	myform = UpdateForm()
# 	daydata = Daydata.query.filter_by(id=id).first()
# 	if daydata.user == str(current_user.name):
# 		if request.method == 'GET':
# 			myform.worktime0.data = daydata.worktime0
# 			myform.worktime1.data = daydata.worktime1
# 			myform.worktime2.data = daydata.worktime2
# 			myform.worktime3.data = daydata.worktime3
# 			myform.completed0.data = daydata.completed0
# 			myform.completed1.data = daydata.completed1
# 			myform.completed2.data = daydata.completed2
# 			myform.completed3.data = daydata.completed3
# 			myform.something0.data = daydata.something0
# 			myform.something1.data = daydata.something1
# 			myform.something2.data = daydata.something2
# 			myform.something3.data = daydata.something3
# 			myform.more0.data = daydata.more0
# 			myform.more1.data = daydata.more1
# 			myform.more2.data = daydata.more2
# 		if  request.method == 'POST':
# 				if myform.validate_on_submit():
# 					wtime=0
# 					for i in [myform.worktime0.data,myform.worktime1.data,myform.worktime2.data,myform.worktime3.data,myform.more1.data]:
# 						if i !="":
# 							wtime=wtime+float(i)
# 					a=0
# 					c=0
# 					for b in [myform.completed0.data,myform.completed1.data,myform.completed2.data,myform.completed3.data,myform.more2.data]:
# 						if b !="":
# 							c=c+int(b)
# 							a=a+1
# 					if c == 0:
# 						com = c
# 					else:
# 						com=c/a
# 					daydata.worktime0=request.form['worktime0']
# 					daydata.worktime1=request.form['worktime1']
# 					daydata.worktime2=request.form['worktime2']
# 					daydata.worktime3=request.form['worktime3']
# 					daydata.completed0=request.form['completed0']
# 					daydata.completed1=request.form['completed1']
# 					daydata.completed2=request.form['completed2']
# 					daydata.completed3=request.form['completed3']
# 					daydata.something0=request.form['something0']
# 					daydata.something1=request.form['something1']
# 					daydata.something2=request.form['something2']
# 					daydata.something3=request.form['something3']
# 					daydata.more0=request.form['more0']
# 					daydata.more1=request.form['more1']
# 					daydata.more2=request.form['more2']
# 					daydata.worktime=wtime
# 					daydata.completed=com
# 					daydata.time=datetime.now()
# 					db.session.add(daydata)
# 					db.session.commit()
# 					if int(time.strftime("%W")) == daydata.yearweek:
# 						return redirect(url_for('main.index'))
# 					elif (int(time.strftime("%W"))-1) == daydata.yearweek:
# 						return redirect(url_for('zhoubaos.zbdata',name=str(current_user.name)))
# 					elif int(time.strftime("%W")) == 1 and daydata.yearweek == 52:
# 						return redirect(url_for('zhoubaos.zbdata', name=str(current_user.name)))
# 					else:
# 						return redirect(url_for('main.index'))
# 				else:
# 					# print myform.errors
# 					flash(u'修改数据失败！'+myform.errors.values()[0][0])
# 					return render_template('update.html',form=myform)
# 		return render_template('update.html', form=myform)
# 	else:
# 		flash("没有权限！")
# 		return redirect(url_for('main.index'))
#
# @main.route('/deldata/<id>')
# @login_required
# def delid(id):
# 	deldata = Daydata.query.filter_by(id=id).first()
# 	if deldata.user == str(current_user.name):
# 		db.session.delete(deldata)
# 		db.session.commit()
# 		return redirect(url_for('main.index'))
# 	else:
# 		flash("没有权限！")
# 		return redirect(url_for('main.index'))