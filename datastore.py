import os
import time
import calendar
import datetime
from xml.dom.minidom import parse 


class DataStore: 

    def __init__(self):
        self._measurements = {}
    
    def load(self, datafile): 
        f = open(datafile)
        dom = parse(f)
        nodes = dom.getElementsByTagName("IntervalReading") 
        val_func  = lambda n: n.getElementsByTagName("value")[0].childNodes[0].nodeValue
        start_func = lambda n: n.getElementsByTagName("start")[0].childNodes[0].nodeValue
        start  = map(start_func,nodes)
        self._measurements = zip(map(start_func, nodes), map(val_func,nodes))
   
    def get_year(self, year):
        f = lambda x: time.gmtime(float(x))
        year_filter = lambda x: f(x[0]).tm_year == year 
        year_data = filter(year_filter, self._measurements) 
        rollup = dict([(i, []) for i in range(1,13)]) 
        for x in dict(year_data).iteritems(): 
            rollup[time.gmtime(float(x[0])).tm_mon].append(x[1]) 
        
        for x in rollup.iteritems():
            rollup[x[0]] = sum(map(int, x[1])) 
         
        return rollup 
    
    def get_month(self, year, month):
        f = lambda x: time.gmtime(float(x))
        year_filter = lambda x: f(x[0]).tm_year == year 
        month_filter = lambda x: f(x[0]).tm_mon == month 
        month_data = filter(year_filter, filter(month_filter, self._measurements))
        days_in_month = calendar.monthrange(year, month)[1]
        rollup = dict([(i, []) for i in range(1,days_in_month +1)]) 
        for x in dict(month_data).iteritems(): 
            rollup[time.gmtime(float(x[0])).tm_mday].append(x[1]) 
        
        for x in rollup.iteritems():
            rollup[x[0]] = sum(map(int, x[1])) 
         
        return rollup 
    
    def get_week(self, year, week): 
        f = lambda x: time.gmtime(float(x))
        week_filter = lambda x: datetime.date(f(x[0]).tm_year, f(x[0]).tm_mon, f(x[0]).tm_mday).isocalendar()[1] == week  
        year_filter = lambda x: f(x[0]).tm_year == year 
        week_data = filter(year_filter, filter(week_filter, self._measurements))  
 
        rollup = dict([(i, []) for i in range(7)]) 
        for x in dict(week_data).iteritems():
            rollup[f(x[0]).tm_wday].append(x[1]) 
        
        for x in rollup.iteritems():
            rollup[x[0]] = sum(map(int, x[1]))
         
        return rollup

    def get_day(self, year, day): 
        f = lambda x: time.gmtime(float(x))
        year_filter = lambda x: f(x[0]).tm_year == year 
        day_filter = lambda x: f(x[0]).tm_yday == day
        day_data = filter(year_filter, filter(day_filter, self._measurements))  
        rollup = dict([(i, []) for i in range(24)]) 

        for x in dict(day_data).iteritems():
            rollup[f(x[0]).tm_hour].append(x[1])
        for x in rollup.iteritems():
            rollup[x[0]] = sum(map(int, x[1]))
        
        return rollup 
    
    
