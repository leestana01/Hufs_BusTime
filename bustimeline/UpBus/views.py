import xml.etree.ElementTree as ET
from django.shortcuts import render
import urllib.parse
from .apicaller import APICaller

#수정!! 확인바람

def bus_list(request):

    # 버스 번호와 정류장 정보
    bus_numbers = [1303, 1117, 1150, 1005]
    bus_stops = ['외대사거리', '모현사거리', '기숙사', '도서관', '파란지붕']

    # 실시간 버스 위치 정보를 저장할 딕셔너리
    bus_locations_Down = APICaller(228000345) #하행 종점 | 외대.모현빌라
    bus_locations_Up = APICaller(228000349) #상행 종점 | 한국외대종점
    bus_locations_info = APICaller(228000352)
    print('------------------------API 호출 끝!---------------------------')
    
    downList1 = [[],[],[],[],[]]
    downList2 = []
    for idx, inList in enumerate(downList1):
        for bus in bus_numbers:
            if bus_locations_Down[str(bus)].get('location') == str(4 - idx):
                inList.append(bus)
    for idx, inList in enumerate(downList1):
        if idx == 1:
            continue
        downList2.append(inList)
    print('하행버스-정류장 리스트화 (변환 전)')
    print(downList1)
    print('하행버스-정류장 리스트화 (변환 후)')
    print(downList2)

    print('상행버스-정류장 리스트화')
    upList = [[],[],[],[],[]]
    for idx, inList in enumerate(upList):
        for bus in bus_numbers:
            if bus_locations_Up[str(bus)].get('location') == str(idx):
                inList.append(bus)
    print(upList)
        

    context = {
        'bus_numbers': bus_numbers,
        'bus_stops': bus_stops,
        'downList' : downList2,
        'upList' : upList,
        'upInfo' : bus_locations_info,
    }

    return render(request, 'bus_list.html', context)