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
    bus_locations_Up = APICaller(228000349) #상행 종점 | 한국외대종점
    bus_locations_Down = APICaller(228000346) #하행 종점 | 외대.모현빌라
    bus_locations = [bus_locations_Down, bus_locations_Up]
    
    # 버스 위치 정보를 담을 딕셔너리 초기화
    bus_locations_info = {}
    
    #api caller에서 location만 받아오기
    location_1303 = bus_locations_Down.get("1303", {}).get("location")
    location_1117 = bus_locations_Down.get("1117", {}).get("location")
    location_1150 = bus_locations_Down.get("1150", {}).get("location")
    location_1005 = bus_locations_Down.get("1005", {}).get("location")
    
    location_1303 = bus_locations_Up.get("1303", {}).get("location")
    location_1117 = bus_locations_Up.get("1117", {}).get("location")
    location_1150 = bus_locations_Up.get("1150", {}).get("location")
    location_1005 = bus_locations_Up.get("1005", {}).get("location")


    # 버스 위치 정보 추가
    for bus_location in bus_locations:
        for bus_number, location_info in bus_location.items():
            if 'location' in location_info and location_info['location'] != 'N/A':
                location = int(location_info['location'])  # 현재 위치를 정수로 변환
                if location > 0:  # 현재 위치가 양수인 경우에만 정류장에 표시
                    bus_locations_info[str(bus_number)] = str(bus_stops[location-1])

    context = {
        'bus_numbers': bus_numbers,
        'bus_stops': bus_stops,
        'bus_locations_info': bus_locations_info,
        'location_1303': location_1303,
        'location_1117': location_1117,
        'location_1150': location_1150,
        'location_1005': location_1005,
    }

    return render(request, 'bus_list.html', context)