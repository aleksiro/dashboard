from django.shortcuts import render, HttpResponse

def dashboard(request):
    return render(request, 'dashboard.html')

def dashboard_test(request):
    return render(request, 'dashboard_test.html')
