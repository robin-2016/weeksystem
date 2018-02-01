import time
from .. import db
from ..models import Groups,Newdata

def getlastweektime():
	if int(time.strftime("%W")) == 1:
		yearweek = 52
	else:
		yearweek = int(time.strftime("%W")) - 1
	return yearweek

def huizong(name,yearweek):
	# yearweek = getlastweektime()
	data = db.session.query(Newdata).filter_by(user=name).filter_by(
			yearweek=yearweek).order_by(Newdata.week).all()
	week = {}
	for a in data:
		week[a.week] = a.week
	weekjilu = 0
	weekdata = []
	while weekjilu < len(week):
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
				worktime = worktime + float(b.worktime)
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

def getgroups(id):
	gname = Groups.query.filter_by(id=id).first().name
	return gname