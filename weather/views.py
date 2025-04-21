import logging

from django.core.cache import cache
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import get_weather_data

logger = logging.getLogger(__name__)
class WeatherView(APIView):
    def get(self, request, location):
        logger.info(f"Sucessfully retrieved weather data for {location} via service.")
        cache_key = f"weather_data:{location.lower().replace('','_')}"
        logger.debug(f"Checking cache for key: {cache_key}")

        # check cache data
        cached_data = cache.get(cache_key)

        if cached_data:
            logger.info(f"Cache hit for location: {location}")
            return Response(cached_data)
        else: 
            logger.info(f"Cache miss for location: {location}. Fetching from API...")


        weather_data = get_weather_data(location)

        if weather_data:
            logger.info(f"Successfully retrieved weather data for {location} via service.")

            cache_timeout = 60 * 60 * 12 # 12 hours
            cache.set(cache_key, weather_data, timeout=cache_timeout)
            logger.info(f"Cached data for {location} with timeout {cache_timeout} seconds.")
            return Response(weather_data, status=status.HTTP_200_OK)

        else:
            logger.error(f"Failed to retrieve weather data for {location}.")
            return Response(
                {"error": "Could not fetch weather data."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

