from django.db import models

class Bus(models.Model):
    number = models.CharField(max_length=10)
    routeId = models.CharField(max_length=50)
    staOrder = models.CharField(max_length=50)