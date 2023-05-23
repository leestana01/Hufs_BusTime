import requests
from django.conf import settings
from bs4 import BeautifulSoup
from .models import Bus


# API를 호출하는 함수. 아래와 같은 형식으로 반환함
# { 
#   버스번호1:{location:몇정거장전? , predict_time:예상시간?},
#   버스번호2:{location:몇정거장전? , predict_time:예상시간?},
# } 

testMode = 0 # 0이면 실시간 데이터, 1이면 샘플 데이터
serviceKey = settings.SERVICE_KEY

def APICaller(stationId):
    if testMode:
        return {'1005': {'location': '0', 'predict_time': '999'}, '1117': {'location': '3', 'predict_time': '999'}, '1150': {'location': '3', 'predict_time': '999'}, '1303': {'location': '4', 'predict_time': '999'}}
    base_url = f'http://apis.data.go.kr/6410000/busarrivalservice/getBusArrivalList?serviceKey={serviceKey}'
    initDict = {'location':100, 'predict_time':999}
    results = {bus.number : initDict for bus in Bus.objects.all()}

    response = requests.get(base_url, {'stationId':stationId})
    soup = BeautifulSoup(response.content, 'xml')

    busArrivalList = soup.find_all('busArrivalList')
    for busArrival in busArrivalList:
        routeId = busArrival.find('routeId').text
        locationNo1 = busArrival.find('locationNo1').text
        predictTime1 = busArrival.find('predictTime1').text
        bus = Bus.objects.filter(routeId=routeId)
        if (bus):
            busNumber = bus.first().number
            results[busNumber] = {'location': locationNo1, 'predict_time': predictTime1}
    print(results)
    return results


