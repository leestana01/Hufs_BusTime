from django.shortcuts import render

from .models import BusList, NowDay
from datetime import datetime

def busListView(request):
    now_time = datetime.now().time()

    day_type = checkDay() # 요일 반환

    buses = BusList.objects.filter(day_type=day_type).order_by('bus_time')
    # day_type(요일)에 해당하는 것들만 필터링해줍니다.
    # 이후 버스 시간 순서대로 정렬합니다.
    # 버스를 현 시간 이후것들만 보여주고 싶다면 필터에 ', bus_time__gte=now_time' 를 추가하세요
    
    formatted_time = now_time.strftime("%H시 %M분") # 기준시간 표시를 위한 문자열 포맷팅
    return render(request, 'bus_list.html', {'buses': buses, 'now_time' : formatted_time})


# 메인 페이지 잠깐 쓰려고 만들었습니다. 지우려면 지우세요.
def mainPage(request):
    return render(request, 'mainpage.html')




# -----------------------------------------------------------------
# 일반 함수 호출 영역입니다


# 주중, 토요일, 일요일 체크하여 day_type을 반환하는 함수
def checkDay():
    today = datetime.today().weekday()

    if today < 5:  # 주중
        day_type = NowDay.objects.get(day_type='WEEK')
    elif today == 5:  # 토요일
        day_type = NowDay.objects.get(day_type='SAT')
    else:  # 일요일
        day_type = NowDay.objects.get(day_type='SUN')    

    return day_type