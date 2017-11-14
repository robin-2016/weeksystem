import time
from flask import render_template,request,redirect,url_for,flash,session,current_app
from flask_login import login_required
from .. import db
from ..zhoubaos import zhoubaos
from ..models import Users,Role,Groups,Daydata

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
		users = db.session.query(Users.name).filter_by(groups_id=groupid.id).order_by(User.name).paginate(page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
                usersitem=users.items
		return render_template('zbusers.html',usersitem=usersitem,paginate=users)

@zhoubaos.route('/<name>')
@login_required
def zbdata(name):
	data = db.session.query(Daydata,Groups.name).filter_by(user=str(name)).filter_by(yearweek=(int(time.strftime("%W"))-1)).order_by(Daydata.week).outerjoin(Groups,Daydata.project_id==Groups.id).limit(7).all()
	return render_template('zbdata.html',data=data,name=name)

@zhoubaos.route('/groups/<name>')
@login_required
def zbdata_groups(name):
	data = db.session.query(Daydata,Groups.name).filter_by(user=str(name)).filter_by(yearweek=(int(time.strftime("%W"))-1)).order_by(Daydata.week).outerjoin(Groups,Daydata.project_id==Groups.id).limit(7).all()
	return render_template('zbdata_groups.html',data=data,name=name)
