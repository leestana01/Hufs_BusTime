import xml.etree.ElementTree as ET
from django.shortcuts import render
import urllib.parse
from .apicaller import APICaller


def bus_list(request):
    
    # stationId= [29554, 29555, 47061, 47060, 29560, 47606, 29561]       # 수혁 : 이건 정류장id임. stationId 써야함.
    # 버스 번호와 정류장 정보
    bus_numbers1 = [1303, 1117, 1150, 1005]
    bus_numbers2 = [1303, 1117, 1150, 1005]
    bus_stops = ['외대사거리', '모현사거리', '기숙사', '도서관', '파란지붕']

    # 실시간 버스 위치 정보를 저장할 딕셔너리
    bus_locations_Up = APICaller(228000349) #상행 종점 | 한국외대종점
    bus_locations_Down = APICaller(228000346) #하행 종점 | 외대.모현빌라
    bus_locations = [bus_locations_Down, bus_locations_Up]
            

    bus_number_ranges = {
        bus_number: list(range(bus_number + 1, bus_number + 5))
        for bus_number in bus_numbers1 + bus_numbers2
    }

    context = {
        'bus_numbers1': bus_numbers1,
        'bus_numbers2': bus_numbers2,
        'bus_locations': bus_locations,
        'bus_stops': bus_stops,
        'bus_number_ranges': bus_number_ranges,
    }

    return render(request, 'bus_list.html', context)

def parse_bus_location(response_text):
    bus_location = 'N/A'

    if response_text:
        root = ET.fromstring(response_text)
        item_nodes = root.findall('.//itemList')
        for item_node in item_nodes:
            bus_location_node = item_node.find('locationNo1')

            if bus_location_node is not None:
                bus_location = bus_location_node.text

    return bus_location, None