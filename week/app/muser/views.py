#!/usr/bin/python
#-*-coding:utf-8-*-
from flask import render_template,request,redirect,url_for,flash,current_app,session
from flask_login import login_required
from .. import db
from ..muser import muser
from ..models import Users,Role,Groups
from .forms import MuserForm
from werkzeug.security import generate_password_hash

@muser.route('/main')
@login_required
def musermain():
	page = request.args.get('page',1,type=int)
#	users = db.session.query(Users.id,Users.name,Role.name,Groups.name,Users.uptime).outerjoin(Role,Users.role_id==Role.id).outerjoin(Groups,Users.groups_id==Groups.id).all()
	users = db.session.query(Users.id,Users.name,Role.name,Groups.name,Users.uptime).outerjoin(Role,Users.role_id==Role.id).outerjoin(Groups,Users.groups_id==Groups.id).order_by(Groups.name).paginate(page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
	usersitem = users.items
	return render_template('muser.html',usersitem=usersitem,pagination=users)

@muser.route('/auth/<id>',methods=['GET','POST'])
@login_required
def usersdo(id):
	myform=MuserForm()
	udata=Users.query.filter_by(id=id).first()
	if request.method == 'GET':	
		myform.name.data=udata.name
		if udata.role_id == None:
			myform.role.data = 0
		else:
			myform.role.data=udata.role_id
		if udata.groups_id==None:
			myform.groups.data=0
		else:
			myform.groups.data=udata.groups_id
	if request.method == 'POST':
		if myform.validate_on_submit():
			udata.role_id=request.form['role']
			udata.groups_id=request.form['groups']
			db.session.add(udata)
			db.session.commit()
			flash("修改成功！")
			return redirect(url_for('muser.musermain'))
		else:
			flash('Update fialed!!!')
			return render_template('muserdo.html',myform=myform)
	return render_template('muserdo.html',myform=myform)

@muser.route('/pw/<id>')
@login_required
def mpw(id):
	if session['role'] =='admin':
		userchangepw = Users.query.filter_by(id=id).first()
		userchangepw.password_hash=str(0)
		db.session.add(userchangepw)
		db.session.commit()
		flash("重置成功！")
		return redirect(url_for('muser.musermain'))
	else:
		flash("没有权限！")
		return redirect(url_for('muser.musermain'))