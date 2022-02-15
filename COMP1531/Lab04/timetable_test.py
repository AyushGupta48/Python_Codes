import pytest
from timetable import timetable
from datetime import date, time, datetime

def test_given():
   assert (timetable([date(2019,9,27), date(2019,9,30)], [time(14,10), time(10,30)]))\
    == [datetime(2019,9,27,10,30), datetime(2019,9,27,14,10), datetime(2019,9,30,10,30),\
     datetime(2019,9,30,14,10)]

def test_single_date():
   assert(timetable([date(2021,2,12)], [time(14,10)])) == [datetime(2021,2,12,14,10)]

def test_empty_string():
   assert(timetable([],[])) == []
