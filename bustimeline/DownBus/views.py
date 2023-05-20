import requests
import xml.etree.ElementTree as ET
from django.shortcuts import render
import urllib.parse


def mainPage(request):
    return render(request, 'mainPage.html')

def bus_list(request):
    # API 서비스 키
    SERVICE_KEY = "NtJsRbGCOEUzaVWZV0YH%2BohG0HsEnbQsxLeHFL3y%2F1HHMeyRALLGqSGZs3qMMIFG%2FBoyQ8KBgfs29NRRsTwsOw%3D%3D"
    
    stationId= [29554, 29555, 47061, 47060, 29560, 47606, 29561]
    # 버스 번호와 정류장 정보
    bus_numbers1 = [1303, 1117, 1150, 1005]
    bus_numbers2 = [1303, 1117, 1150, 1005]
    bus_stops = ['외대사거리', '모현사거리', '기숙사', '도서관', '파란지붕']

    # 실시간 버스 위치 정보를 저장할 딕셔너리
    bus_locations = APICaller(stationId, SERVICE_KEY)
            

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

def APICaller(stationId, serviceKey):
    base_url = f'http://apis.data.go.kr/6410000/busarrivalservice/getBusArrivalItem'

    results = {}
    for bus_number in [1117, 1303, 1150, 1005]:
        params = {
            'serviceKey': serviceKey,
            'stationId': stationId,
            'routeId': bus_number
        }
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        bus_location, predict_time = parse_bus_location(response.text)
        results[bus_number] = {'location': bus_location, 'predict_time': predict_time}

    return results


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