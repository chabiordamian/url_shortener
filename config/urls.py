from django.urls import include, path

urlpatterns = [
    path('', include('shortener.urls')),
]
