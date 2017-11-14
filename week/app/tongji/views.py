#-*-coding=utf-8-*-
import time,datetime,os
from collections import Counter
from flask import render_template,request,redirect,url_for,flash
from flask_login import login_required
from .. import db
from ..tongji import tongji
from ..models import Users,Role,Groups,Daydata
from .forms import TongjiForm

weekday = 5
yweek = int(time.strftime("%W"))-1

@tongji.route('/tongji',methods=['GET','POST'])
@login_required
def tongji01():
	myform = TongjiForm()
	myform.weekday.data = 5
	if myform.validate_on_submit():
		if myform.weekday.data != None or myform.weekday.data != 5:
			global weekday
			global yweek
			weekday = int(request.form['weekday'])
			yweek = myform.yweek.data
		return redirect(url_for('tongji.compute'))
	return render_template('tongji.html',myform=myform)

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
	if yweek == (int(time.strftime("%W"))-1):
		tweek = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
		yweeklabel=u'上周'
	elif yweek == (int(time.strftime("%W"))-2):
		tweek = datetime.date.today() - datetime.timedelta(days=(datetime.date.today().weekday()+7))
		yweeklabel=u'上上周'
	else:
		tweek = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
		yweeklabel=u'上周'
	print yweek
	montime=(datetime.datetime.strptime(str(tweek),'%Y-%m-%d')).replace(hour=9,minute=30,second=00)
#	print montime
#	users = Users.query.all()
	users = db.session.query(Users.name,Groups.name).outerjoin(Groups,Users.groups_id==Groups.id).all()
	for i in users:
		data = db.session.query(Daydata.worktime,Daydata.time).filter_by(user=str(i[0])).filter_by(yearweek=yweek).order_by(Daydata.week.desc()).limit(7).all()
		if data != []:
			tlist = []
			for b in data:
				tlist.append(b.time)
			maxtlist = max(tlist)
			if maxtlist > montime:
				uptime.append((i[0],i[1],maxtlist))
		else:
			uptime.append((i[0],i[1],''))
		if len(data) < weekday:
			zhoubao.append((i[0],i[1],(weekday-len(data))))
		wk = int(0)
		for a in data:
			wk = wk + a.worktime
		if wk < weekday*8:
			wtime.append((i[0],i[1],(weekday*8-wk)))
	if os.path.exists('/root/week/zbdata/')==False:
		os.makedirs('/root/week/zbdata/') 
	with open('/root/week/zbdata/'+str(yweek),'w') as f:
		f.write(str(uptime)+'\n')
		f.write(str(zhoubao)+'\n')
		f.write(str(wtime)+'\n')
	return render_template('result.html',uptime=uptime,zhoubao=zhoubao,wtime=wtime,yweeklabel=yweeklabel)	

def qiuhe(l):
	lists_c = []
	list_new = []
        b=0
        for i in range(len(l)):
		if [l[i][0],l[i][1]] not in list_new:
			list_new.append([l[i][0],l[i][1]])
        for n in range(len(list_new)):
		a=0
		for m in range(len(l)):
			if list_new[n][0]==l[m][0]:
				a = a + l[m][2]
		lists_c.append([list_new[n][0],list_new[n][1],a])
	return lists_c

@tongji.route('/yuetongji')
@login_required
def hebing():
	uptimes =[]
	zhoubaos = []
	wtimes = []
	linshi = []
	uptimes_c =[]
	mlast = datetime.date.today() - datetime.timedelta(days=datetime.datetime.now().day)
	mfirst = mlast - datetime.timedelta(days=mlast.day-1)
#	print mlast.strftime("%W")
#	print mlast.strftime("%w")
#	print type(mlast.strftime("%w"))
#	print mfirst.strftime("%W")
#	print mfirst.strftime("%w")
#	print mfirst-datetime.timedelta(days=-1)
#	print (mfirst-datetime.timedelta(days=-1)).strftime("%W")
#	print mfirst-datetime.timedelta(days=1)
#	print (mfirst-datetime.timedelta(days=1)).strftime("%W")
	if int(mfirst.strftime("%w")) >3:
		fweek = int(mfirst.strftime("%W"))+1
	elif int(mfirst.strftime("%w"))==0:
		fweek = int(mfirst.strftime("%W"))+1
	else:
		fweek = int(mfirst.strftime("%W"))
	if int(mlast.strftime("%w")) <3:
		lweek = int(mlast.strftime("%W"))
	elif int(mlast.strftime("%w")) == 0:
		lweek = int(mlast.strftime("%W"))+1
	else:
		lweek = int(mlast.strftime("%W"))+1
#	print fweek,lweek
#	print range(fweek,lweek)
#	shangzhou= int(time.strftime("%W"))-1
	for i in range(fweek,lweek):
		if os.path.exists('/root/week/zbdata/'+str(i)):
			with open('/root/week/zbdata/'+str(i),'r') as f:
				linshi = f.readlines()
				uptimes = uptimes +eval(linshi[0])
				zhoubaos=zhoubaos + eval(linshi[1])
				wtimes=wtimes + eval(linshi[2])
#	print uptimes
#	print zhoubaos
#	print wtimes
	for i in uptimes:
		uptimes_c.append(i[0])
	zhoubao=qiuhe(zhoubaos)
	wtime=qiuhe(wtimes)
#	print zhoubao
#	print wtime
#	print Counter(uptimes_c)
	uptime = Counter(uptimes_c)
	return render_template('yueresult.html',uptime=uptime,zhoubao=zhoubao,wtime=wtime)	
