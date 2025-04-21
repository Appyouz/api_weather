import logging

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import get_weather_data

logger = logging.getLogger(__name__)
class WeatherView(APIView):
    def get(self, request, location):
        logger.info(f"Sucessfully retrieved weather data for {location} via service.")
        weather_data = get_weather_data(location)

        if weather_data:
            logger.info(f"Successfully retrieved weather data for {location} via service.")
            return Response(weather_data, status=status.HTTP_200_OK)

        else:
            logger.error(f"Failed to retrieve weather data for {location}.")
            return Response(
                {"error": "Could not fetch weather data."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

