#!/usr/bin/python
#-*-coding:utf-8 -*-
from datetime import datetime
import time
from ..main import main
from flask import render_template,request,redirect,url_for,flash
from flask_login import login_required,current_user
from .. import db
from ..models import Daydata,Groups,Users
from .forms import InsertForm,UpdateForm

@main.route('/main')
@login_required
def index():
	if current_user.get_id() != None:
		data = db.session.query(Daydata,Groups.name).filter_by(user=str(current_user.name)).filter_by(yearweek=int(time.strftime("%W"))).order_by(Daydata.week).outerjoin(Groups,Daydata.project_id==Groups.id).limit(7).all()
		return render_template('main.html',data=data)
	else:
		return redirect(url_for('login.denglu'))
		flash("Data is nothing!!!")
#                return render_template('main.html',data=data)

@main.route('/insert',methods = ['GET','POST'])
@login_required
def insert():
	myform = InsertForm()
	projectid=Users.query.filter_by(name=(str(current_user.name))).first()
	if request.method == 'GET':
		myform.project.data=projectid.groups_id
	if request.method == 'POST':
		if myform.validate_on_submit():
			if Daydata.query.filter_by(user=str(current_user.name)).filter_by(yearweek=int(request.form['yearweek'])).filter_by(week=request.form['week']).first() is None:
				wtime=0
				for i in [myform.worktime0.data,myform.worktime1.data,myform.worktime2.data,myform.worktime3.data]:
					if i is not None:
						wtime=wtime+i
				a=0
				c=0
				for b in [myform.completed0.data,myform.completed1.data,myform.completed2.data,myform.completed3.data]:
					if b is not None:
						c=c+b
						a=a+1
				if c == 0:
					com = c
				else:
					com=c/a
				dinsert = Daydata(user=str(current_user.name),
					yearweek=myform.yearweek.data,
					week=myform.week.data,
					project_id=myform.project.data,
					worktime=wtime,
					worktime0=myform.worktime0.data,
					worktime1=myform.worktime1.data,
					worktime2=myform.worktime2.data,
					worktime3=myform.worktime3.data,
					completed0=myform.completed0.data,
					completed1=myform.completed1.data,
					completed2=myform.completed2.data,
					completed3=myform.completed3.data,
					something0=myform.something0.data,
					something1=myform.something1.data,
					something2=myform.something2.data,
					something3=myform.something3.data,
					more0=myform.more0.data,
					more1=myform.more1.data,
					more2=myform.more2.data,
					completed=com,
					time=datetime.now())
				db.session.add(dinsert)
				db.session.commit()
			#flash("Insert Successful!")
				if int(time.strftime("%W")) == myform.yearweek.data:
					return redirect(url_for('main.index'))
				elif (int(time.strftime("%W"))-1) == myform.yearweek.data:
					return redirect(url_for('zhoubaos.zbdata',name=str(current_user.name)))
				else:
					return redirect(url_for('main.index'))
			else:
				flash(u'星期数据重复！请修改。')
				return render_template('insert.html',form=myform)
		else:
			print myform.errors
			flash(u'增加数据失败！')
			return render_template('insert.html',form=myform)
	
	return render_template('insert.html',form=myform)

@main.route('/update/<id>',methods=['GET','POST'])
@login_required
def update(id):
	myform = UpdateForm()
	daydata = Daydata.query.filter_by(id=id).first()
	if request.method == 'GET':
		myform.worktime0.data = daydata.worktime0
		myform.worktime1.data = daydata.worktime1
		myform.worktime2.data = daydata.worktime2
		myform.worktime3.data = daydata.worktime3
		myform.completed0.data = daydata.completed0
		myform.completed1.data = daydata.completed1
		myform.completed2.data = daydata.completed2
		myform.completed3.data = daydata.completed3
		myform.something0.data = daydata.something0
		myform.something1.data = daydata.something1
		myform.something2.data = daydata.something2
		myform.something3.data = daydata.something3
		myform.more0.data = daydata.more0
		myform.more1.data = daydata.more1
		myform.more2.data = daydata.more2
	if  request.method == 'POST':
			if myform.validate_on_submit():
				wtime=0
				for i in [myform.worktime0.data,myform.worktime1.data,myform.worktime2.data,myform.worktime3.data]:
					if i is not None:
						wtime=wtime+i
				a=0
				c=0
				for b in [myform.completed0.data,myform.completed1.data,myform.completed2.data,myform.completed3.data]:
					if b is not None:
						c=c+b
						a=a+1
				if c == 0:
					com = c
				else:
					com=c/a
				if request.form['worktime0'] != '':
					daydata.worktime0=request.form['worktime0']
				if request.form['worktime1'] != '':
					daydata.worktime1=request.form['worktime1']
				if request.form['worktime2'] != '':
					daydata.worktime2=request.form['worktime2']
				if request.form['worktime3'] != '':
					daydata.worktime3=request.form['worktime3']
				if request.form['completed0'] != '':
					daydata.completed0=request.form['completed0']
				if request.form['completed1'] != '':
					daydata.completed1=request.form['completed1']
				if request.form['completed2'] != '':
					daydata.completed2=request.form['completed2']
				if request.form['completed3'] != '':
					daydata.completed3=request.form['completed3']
				if request.form['something0'] != '':
					daydata.something0=request.form['something0']
				if request.form['something1'] != '':
					daydata.something1=request.form['something1']
				if request.form['something2'] != '':
					daydata.something2=request.form['something2']
				if request.form['something3'] != '':
					daydata.something3=request.form['something3']
				if request.form['more0'] != '':
					daydata.more0=request.form['more0']
				if request.form['more1'] != '':
					daydata.more1=request.form['more1']
				if request.form['more2'] != '':
					daydata.more2=request.form['more2']
				daydata.worktime=wtime
				daydata.completed=com
				daydata.time=datetime.now()
				db.session.add(daydata)
				db.session.commit()
				if int(time.strftime("%W")) == daydata.yearweek:
					return redirect(url_for('main.index'))
				elif (int(time.strftime("%W"))-1) == daydata.yearweek:
					return redirect(url_for('zhoubaos.zbdata',name=str(current_user.name)))
				else:
					return redirect(url_for('main.index'))
#				return redirect(url_for('main.index'))
			else:
				print myform.errors
				flash(u'修改数据失败！')
				return render_template('update.html',form=myform)
	return render_template('update.html',form=myform)
