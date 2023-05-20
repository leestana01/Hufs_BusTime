import requests
from django.conf import settings
from bs4 import BeautifulSoup
from .models import Bus


# API를 호출하는 함수. 아래와 같은 형식으로 반환함
# { 
#   버스번호1:{location:몇정거장전? , predict_time:예상시간?},
#   버스번호2:{location:몇정거장전? , predict_time:예상시간?},
# } 
def APICaller(stationId):
    buses = Bus.objects.all()
    serviceKey = settings.SERVICE_KEY
    base_url = f'http://apis.data.go.kr/6410000/busarrivalservice/getBusArrivalItem?serviceKey={serviceKey}'

    results = {}
    for bus in buses:
        params = {
            'stationId': stationId,
            'routeId': bus.routeId,
            'staOrder': bus.staOrder
        }
        response = requests.get(base_url, params=params)
        soup = BeautifulSoup(response.content, 'xml')

        try:
            locationNo1 = soup.find('locationNo1').text
            predictTime1 = soup.find('predictTime1').text
        except AttributeError as e:
            print(f"Error: {e}")
            locationNo1 = 'N/A'
            predictTime1 = 'N/A'
        results[bus.number] = {'location': locationNo1, 'predict_time': predictTime1}
        # location      : 몇 번째 전?
        # predict_time  : 예상 시간
    return results
