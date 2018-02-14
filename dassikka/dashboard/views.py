from django.shortcuts import render, HttpResponse, render_to_response
from dashboard import models
from django.template.response import TemplateResponse

def dashboard(request):
    return render(request, 'dashboard.html')

def dashboard_test(request):
    data =  models.busscheduletable.objects.all()
    return TemplateResponse(request, 'dashboard_test.html', {"data": data})
