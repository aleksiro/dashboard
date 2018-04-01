from django.shortcuts import render, HttpResponse, render_to_response
from dashboard import models
from django.template.response import TemplateResponse
from django.db import connections
from django.db.models import Count
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max

def dashboard(request):
    data = {
        'busdata': models.busscheduletable.objects.filter(loadtime=models.busscheduletable.objects.all().aggregate(Max('loadtime'))['loadtime__max']),
        'weatherdata': models.weathertable.objects.filter(loadtime=models.weathertable.objects.all().aggregate(Max('loadtime'))['loadtime__max'])
    }
    return render_to_response('dashboard.html', data)

def dashboard_test(request):
    data = {
        'busdata': models.busscheduletable.objects.filter(loadtime=models.busscheduletable.objects.all().aggregate(Max('loadtime'))['loadtime__max']),
        'weatherdata': models.weathertable.objects.filter(loadtime=models.weathertable.objects.all().aggregate(Max('loadtime'))['loadtime__max'])
    }
    return render_to_response('dashboard_test.html', data)

def pass_bus_data(request):
    data = models.busscheduletable.objects.filter(loadtime=models.busscheduletable.objects.all().aggregate(Max('loadtime'))['loadtime__max']).all().values("line", "time")
    print(data)
    return JsonResponse(list(data), safe=False)

def pass_weather_data(request):
    data = models.weathertable.objects.filter(loadtime=models.weathertable.objects.all().aggregate(Max('loadtime'))['loadtime__max']).all().values("forecast_type", "temperature", "rf_temperature", "icon_code")
    return JsonResponse(list(data), safe=False)

def pass_sense_data(request):
    data = models.sensehattable.objects.all().values("measuretime", "temperature", "humidity")
    return JsonResponse(list(data), safe=False)
