from django.db import models

class NowDay(models.Model):
    dayCase = [
        ('WEEK', '주중'),
        ('SAT', '토요일'),
        ('SUN', '일요일/공휴일'),
    ]

    day_type = models.CharField(max_length=4, choices=dayCase, verbose_name='요일')


class BusList(models.Model):
    bus_number = models.IntegerField(verbose_name='버스번호')
    bus_time = models.TimeField(verbose_name='출발시간')
    day_type = models.ForeignKey(NowDay, on_delete=models.CASCADE, default='WEEK', verbose_name='요일')

