from django.conf.urls import url
from django_unifi_portal.views import UserAuthorizeView, UnifiUserLogin

urlpatterns = [
    url(r'guest/s/default/$', UserAuthorizeView.as_view(), name='index'),
    url(r'^unifi-portal/login/$', UnifiUserLogin.as_view(), name='unifi_login'),
]
