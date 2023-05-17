from django.shortcuts import render
from django.http import HttpResponse

from .models import Bus
import requests
from bs4 import BeautifulSoup

def bus_arrival(request):
    buses = Bus.objects.all()
    stationId = '228000351'
    serviceKey = 'NtJsRbGCOEUzaVWZV0YH%2BohG0HsEnbQsxLeHFL3y%2F1HHMeyRALLGqSGZs3qMMIFG%2FBoyQ8KBgfs29NRRsTwsOw%3D%3D'
    base_url = f'http://apis.data.go.kr/6410000/busarrivalservice/getBusArrivalItem?serviceKey={serviceKey}'

    results = {}
    for bus in buses:
        params = {
            'stationId': stationId,
            'routeId': bus.routeId,
            'staOrder': bus.staOrder
        }
        response = requests.get(base_url, params=params)
        print(response.request.url)
        print('------------------------------------')
        print(response.content)
        print('------------------------------------')
        soup = BeautifulSoup(response.content, 'xml')
        locationNo1_tag = soup.find('locationNo1')
        print(locationNo1_tag)
        print('------------------------------------')
        print('------------------------------------')
        # return HttpResponse(response.content)

        try:
            locationNo1 = soup.find('locationNo1').text
            predictTime1 = soup.find('predictTime1').text
        except AttributeError as e:
            print(f"Error: {e}")
            locationNo1 = 'N/A'
            predictTime1 = 'N/A'
        results[bus.number] = {'location': locationNo1, 'predict_time': predictTime1}

    return render(request, 'bus_list_up.html', {'results': results})
