#!/usr/bin/python
#-*-coding:utf-8 -*-
import time
from flask import render_template,request,redirect,url_for,flash,session,current_app
from flask_login import login_required,current_user
from .. import db
from ..zhoubaos import zhoubaos
from ..models import Users,Groups,Newdata,Score
from .forms import ScoreForm,TijiaoForm

def getgroups(id):
	gname = Groups.query.filter_by(id=id).first().name
	return gname

def huizong(name):
	if int(time.strftime("%W")) == 1:
		data = db.session.query(Newdata).filter_by(user=name).filter_by(
			yearweek=52).order_by(Newdata.week).all()
	else:
		data = db.session.query(Newdata).filter_by(user=name).filter_by(
			yearweek=int(time.strftime("%W")) - 1).order_by(Newdata.week).all()
	weekjilu = 0
	weekdata = []
	while weekjilu < 7:
		if data == []:
			break
		worktime = 0
		completed = 0
		something = ""
		projectjia = ""
		c = 0
		weekzidian = {}
		for b in data:
			if b.week == weekjilu:
				worktime = worktime + int(b.worktime)
				something = something + b.something + '<br/>'
				completed = completed + int(b.completed)
				projectjia = projectjia + str(getgroups(b.project_id)) + '<br/>'
				c = c + 1
		weekzidian['project_id'] = projectjia
		weekzidian['worktime'] = worktime
		if c == 0:
			weekzidian['completed'] = 0
		else:
			weekzidian['completed'] = completed / c
		weekzidian['something'] = something
		weekzidian['week'] = weekjilu
		weekdata.append(weekzidian)
		weekjilu = weekjilu + 1
	return weekdata

def get_score(name,myform):
	# score_data = db.session.query(Score.score, Score.comment).filter_by(yearweek=int(time.strftime("%W")) - 1).filter_by(user=name).first()
	score_data = Score.query.filter_by(user=name).filter_by(yearweek=int(time.strftime("%W")) - 1).first()
	if score_data == None:
		myform.score.data = None
		myform.comment.data = None
	else:
		myform.score.data = score_data.score
		myform.comment.data = score_data.comment
	return myform

@zhoubaos.route('/search')
@login_required
def zbusers():
	page = request.args.get('page',1,type=int)
	if session['role'] == 'admin' or session['role']=='renli':
#		data = db.session.query(Daydata,Groups.name).order_by('user').outerjoin(Groups,Daydata.project_id==Groups.id).all()
		users = db.session.query(Users.name).order_by(Users.name).paginate(page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
		usersitem=users.items
		return render_template('zbusers.html',usersitem=usersitem,pagination=users)
#	elif session['role'] == 'user':
	else:
		groupid = db.session.query(Groups.id).filter_by(name=str(session['role'])).first()
		if groupid is not None:
			users = db.session.query(Users.name).filter_by(groups_id=groupid.id).order_by(Users.name).paginate(page,
			                                                                                                   per_page=
			                                                                                                   current_app.config[
				                                                                                                   'FLASKY_POSTS_PER_PAGE'],
			                                                                                                   error_out=False)
			usersitem = users.items
			return render_template('zbusers.html', usersitem=usersitem, paginate=users)
		else:
			flash("数据为空！")
			return redirect(url_for('main.index'))

#个人上周周报
@zhoubaos.route('/<name>')
@login_required
def zbdata(name):
	# score_data = Score.query.filter_by(user=name).filter_by(yearweek=int(time.strftime("%W"))-1).first()
	if name == str(current_user.name):
		myform = ScoreForm()
		newform = get_score(name, myform)
		weekdata = huizong(name)
		return render_template('lastweek.html', form=newform,data=weekdata, name=name)
	else:
		flash("没有权限！")
		return redirect(url_for('main.index'))

@zhoubaos.route('/groups/<name>',methods =['GET','POST'])
@login_required
def zbdata_groups(name):
	# if int(time.strftime("%W")) == 1:
	# 	data = db.session.query(Daydata, Groups.name).filter_by(user=str(name)).filter_by(
	# 		yearweek=52).order_by(Daydata.week).outerjoin(Groups,Daydata.project_id == Groups.id).limit(7).all()
	# 	return render_template('zbdata_groups.html', data=data, name=name)
	# else:
	# 	data = db.session.query(Daydata,Groups.name).filter_by(user=str(name)).filter_by(yearweek=(int(time.strftime("%W"))-1)).order_by(Daydata.week).outerjoin(Groups,Daydata.project_id==Groups.id).limit(7).all()
	# 	return render_template('zbdata_groups.html',data=data,name=name)
	myform = TijiaoForm()
	if request.method == 'GET':
		myform = get_score(name,myform)
	if myform.validate_on_submit():
		groups_id = db.session.query(Users.groups_id).filter_by(name=name).first()
		score_data = Score.query.filter_by(user=name).filter_by(yearweek=int(time.strftime("%W")) - 1).first()
		# print score_data
		if score_data != None:
			score_data.user = name
			score_data.score = myform.score.data
			score_data.comment = myform.comment.data
			score_data.groups_id = groups_id.groups_id
			score_data.yearweek = int(time.strftime("%W"))-1
		else:
			score_data = Score(user=name,score=myform.score.data,comment=myform.comment.data,groups_id=groups_id.groups_id,yearweek=int(time.strftime("%W"))-1)
		db.session.add(score_data)
		db.session.commit()
		return redirect(url_for('zhoubaos.zbdata_groups',name=name))
	weekdata = huizong(name)
	return render_template('lastweek-geren.html',form = myform, data=weekdata, name=name)

@zhoubaos.route('/pingfen')
@login_required
def pf_paixu():
	page = request.args.get('page', 1, type=int)
	pingfen = db.session.query(Score.user,Score.score).filter_by(yearweek=int(time.strftime("%W"))-1).order_by(Score.score).paginate(page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
	pingfenitem = pingfen.items
	return render_template('pingfen.html',pingfenitem=pingfenitem,pagination=pingfen)