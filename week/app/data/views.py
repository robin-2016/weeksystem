from . import data
from .. import db
from flask import render_template,jsonify,url_for,redirect,request,current_app
from flask_login import login_required,current_user
from ..models import Newdata,Users,Groups
from .forms import DataForm
import time
from datetime import datetime


@data.route('/table')
@login_required
def btable():
	myform = DataForm()
	project_id = Users.query.filter_by(name=str(current_user.name)).first()
	if request.method=='GET':
		myform.project.data = project_id.groups_id
		myform.completed.data = 100
		return render_template('bootstraptable.html',form =myform)
	return render_template('bootstraptable.html', form=myform)

@data.route('/insert/post',methods=['POST'])
@login_required
def insertpost():
	if request.method == 'POST':
		newdata = Newdata(user=str(current_user.name), project_id=request.form['project'], time=datetime.now(),
                              yearweek =int(time.strftime("%W")),week =request.form['week'],something=request.form['something'],
                              completed = request.form['completed'],worktime=request.form['worktime'])
		db.session.add(newdata)
		db.session.commit()
		# return render_template('bootstraptable.html', form=myform)
		return "ok!"
	return "ok!"
		# return redirect(url_for('data.btable'))

@data.route('/data/zhoubao')
@login_required
def datazhoubao():
	pageNumber = request.args.get('pageNumber', 1, type=int)
	data = db.session.query(Newdata).filter_by(user=str(current_user.name)).filter_by(yearweek=int(time.strftime("%W"))).order_by(Newdata.week).paginate(pageNumber,per_page=18,error_out=False)
	dataitems = data.items
	dlist = []
	for a in dataitems:
		dlist.append({"id":a.id,"project": a.project_id, "worktime": a.worktime, "completed": a.completed, "something": a.something,"week": a.week})
	datajson = {"total": data.total, "rows": dlist}
	return jsonify(datajson)

@data.route('/post',methods=['POST'])
@login_required
def editableup():
	newdata2=Newdata.query.filter_by(id=request.form['id']).first()
	newdata2.project_id = request.form['project']
	newdata2.time=datetime.now()
	newdata2.week=request.form['week']
	newdata2.something=request.form['something']
	newdata2.completed=request.form['completed']
	newdata2.worktime=request.form['worktime']
	db.session.add(newdata2)
	db.session.commit()
	# print request.form
	return 'ok!'

@data.route('/del/newdata',methods=['POST'])
@login_required
def newdatadel():
	dataid = request.form['ids']
	idlist = dataid.encode('utf-8').split(",")
	for i in idlist:
		db.session.delete(Newdata.query.filter_by(id=int(i)).first())
	db.session.commit()
	# print request.form
	return 'ok!'

@data.route('/groups')
@login_required
def groupsq():
	groupdata = Groups.query.all()
	group ={}
	for i in groupdata:
		group[i.id] = i.name
	return jsonify(group)