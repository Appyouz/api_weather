from django.urls import path

from . import views

app_name = 'weather'

urlpatterns = [
    path('<str:location>/', views.WeatherView.as_view(), name='weather_detail'),
]
