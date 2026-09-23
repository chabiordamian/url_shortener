from django.urls import path

from .views import resolve_url, shorten_url

urlpatterns = [
    path('api/urls/', shorten_url, name='shorten-url'),
    path('shrt/<str:short_code>/', resolve_url, name='resolve-url'),
]
