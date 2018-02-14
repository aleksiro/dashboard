from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http import JsonResponse

def login_redirect(request):
    return redirect('/')

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'Käyttäjätunnus on jo käytössä. Valitse toinen'
    return JsonResponse(data)
