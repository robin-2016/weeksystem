import time,datetime
#from .. import db
#from ..models import Users,Daydata,Groups

def tmonday():
#	dt = datetime.datetime.strptime("2012-09-12 21:08:12", "%Y-%m-%d %H:%M:%S")  
	dt = datetime.datetime.now()
#print: 2012 9 12 21 8 12 0 None  
	print (dt.year)  
	print(dt.month)  
	print(dt.day)  
	print(dt.hour)  
	print(dt.minute)  
	print(dt.second)  
	print(dt.microsecond)  
	print(dt.tzinfo)  
	print (dt.date())  
	print (dt.time())  
	print (dt.replace(year = 2013))  
	print (dt.timetuple())  
	print (dt.utctimetuple())  
	print (dt.toordinal())  
	print (dt.weekday())  
	print (dt.isocalendar())  
	print type(dt)
	print (dt.replace(hour=9,minute=30,second=00))
	print dt.time()
	print (datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday()))
	
		
		
if __name__ == '__main__':
	tmonday()
