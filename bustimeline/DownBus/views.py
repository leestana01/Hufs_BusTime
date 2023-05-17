from django.shortcuts import render

from .models import BusList, NowDay
from datetime import datetime

def busListView(request):
    today = datetime.today().weekday()
    now_time = datetime.now().time()

    if today < 5:  # 주중
        day_type = NowDay.objects.get(day_type='WEEK')
    elif today == 5:  # 토요일
        day_type = NowDay.objects.get(day_type='SAT')
    else:  # 일요일
        day_type = NowDay.objects.get(day_type='SUN')

    buses = BusList.objects.filter(day_type=day_type, bus_time__gte=now_time)
    formatted_time = now_time.strftime("%H시 %M분")
    return render(request, 'bus_list.html', {'buses': buses, 'now_time' : formatted_time})

def mainPage(request):
    return render(request, 'mainpage.html')