from django.shortcuts import render, HttpResponse
from django.http import *
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from accounts.forms import RegistrationForm, EditProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib import messages

# Create your views here.
def login_user(request):
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
    return render_to_response('login.html', context_instance=RequestContext(request))


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
        else:
            return render(request, 'accounts/register.html', args)

    else:
        form = RegistrationForm()
        args = {'form': form}
        return render(request, 'accounts/register.html', args)


def profile(request):
    arguments ={'user': request.user}
    return render(request, 'accounts/profile.html', arguments)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/profile/')
        else:
            return render(request, 'accounts/editprofile.html', {'form': form})
    else:
        form = EditProfileForm(instance=request.user)
        return render(request, 'accounts/editprofile.html', {'form': form})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        print("1")
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            print("2")
            return redirect('/profile/')
        else:
            print("3")
            messages.error(request, 'Please correct the error below.')

    else:
        print("4")
        form = PasswordChangeForm(user=request.user)
        return render(request, 'accounts/changepassword.html', {'form': form})
