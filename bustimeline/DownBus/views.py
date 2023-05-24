from django.shortcuts import render
from .models import BusList
from datetime import datetime
from collections import defaultdict

def bus_list_up(request):
    now= datetime.now()
    nowDay = now.weekday()
    if nowDay < 5:
        Buses = BusList.objects.filter(day_type = 3)
    elif nowDay == 5:
        Buses = BusList.objects.filter(day_type = 1)
    elif nowDay == 6:
        Buses = BusList.objects.filter(day_type = 2)

    buses_by_time = defaultdict(list)

    for bus in Buses:
        hour = bus.bus_time.hour
        minute = bus.bus_time.minute
        nowTime = str(hour).zfill(2) + ":" + str(minute).zfill(2)
        buses_by_time[nowTime].append(str(bus.bus_number))

    timeListBefore = [[time, buses] for time, buses in buses_by_time.items()]
    timeList = sorted(timeListBefore, key=lambda x: x[0])


    context = {
        'timeList' : timeList ,
    }

    return render(request, 'bus_list_up.html',context)

def mainPage(request):
    return render(request, 'mainPage.html')