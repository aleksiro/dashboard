"""dassikka URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from dassikka.views import login_redirect, validate_username
import accounts.views
import dashboard.views



urlpatterns = [
    url(r'^$', accounts.views.home),
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('allauth.urls')),
    url(r'^register/$', accounts.views.register, name='register'),
    url(r'^login/$', auth_views.login, {'template_name': 'accounts/login.html'}),
    url(r'^logout/$', auth_views.logout, {'template_name': 'accounts/logout.html'}),

    url(r'^profile/$', accounts.views.profile, name='profile'),
    url(r'^profile/edit/$', accounts.views.edit_profile, name='edit_profile'),
    url(r'^home/$', login_redirect, name='login_redirect'),

    url(r'^profile/password/$', accounts.views.change_password, name='change_password'),
    url(r'^reset-password/$', auth_views.password_reset, name='reset_password'),
    url(r'^reset-password/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset-password/complete/$', auth_views.password_reset_complete, name='password_reset_complete'),

    url(r'^dashboard/$', dashboard.views.dashboard, name='dashboard'),
    url(r'^dashboard/testpage/$', dashboard.views.dashboard_test, name='dashboard_test'),

    url(r'^ajax/validate_username/$', validate_username, name='validate_username'),
]
