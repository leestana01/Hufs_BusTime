import requests
from django.conf import settings
from bs4 import BeautifulSoup
from .models import Bus


# API를 호출하는 함수. 아래와 같은 형식으로 반환함
# { 
#   버스번호1:{location:몇정거장전? , predict_time:예상시간?},
#   버스번호2:{location:몇정거장전? , predict_time:예상시간?},
# } 


serviceKey = settings.SERVICE_KEY

def APICaller(stationId):
    buses = Bus.objects.all()
    base_url = f'http://apis.data.go.kr/6410000/busarrivalservice/getBusArrivalItem?serviceKey={serviceKey}'
    busInfo = getBusInfo(stationId)

    results = {}
    for bus in buses:
        params = {
            'stationId': stationId,
            'routeId': bus.routeId,
            'staOrder': busInfo[bus.routeId]
        }
        
        # print('--------------------------각 bus들-------------------------------')
        # print('버스번호 : '+str(bus.number))
        # print('routeId : '+str(bus.routeId))
        # print('stationId : '+str(stationId))
        # print('strOder : '+str(params['staOrder']))
        response = requests.get(base_url, params=params)
        soup = BeautifulSoup(response.content, 'xml')
        # print('--------------------')
        # print(response.content)
        try:
            locationNo1 = soup.find('locationNo1').text
            predictTime1 = soup.find('predictTime1').text
        except AttributeError as e:
            # print(f"Error: {e}")
            locationNo1 = 'N/A'
            predictTime1 = 'N/A'
        results[bus.number] = {'location': locationNo1, 'predict_time': predictTime1}
        # location      : 몇 번째 전?
        # predict_time  : 예상 시간
    return results

def getBusInfo(stationId):
    base_url = f'http://apis.data.go.kr/6410000/busstationservice/getBusStationViaRouteList?serviceKey={serviceKey}'

    params = {
        'stationId': stationId
    }
    response = requests.get(base_url, params)
    soup = BeautifulSoup(response.content, 'xml')
    # print(response.content)

    result = {}
    busRouteList = soup.find_all('busRouteList')
    # print(busRouteList)
    for busRoute in busRouteList:
        routeId = busRoute.find('routeId').text
        staOrder = busRoute.find('staOrder').text
        result[routeId] = staOrder
    
    # print('--------------------------버스 staOrder 얻는 곳!!-------------------------------')
    # print(result)
    return result
