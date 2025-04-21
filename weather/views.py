# weather/views.py

import logging

from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import (WeatherServiceAPIError, WeatherServiceConnectionError,
                       WeatherServiceError, WeatherServiceTimeoutError,
                       get_weather_data)

logger = logging.getLogger(__name__)

class WeatherView(APIView):
    """
    API view to fetch weather data for a given location, with caching and improved error handling.
    """
    def get(self, request, location):
        """
        Handles GET requests to /api/weather/<location>/
        Checks cache first, then fetches weather data using the service,
        and caches the result. Handles specific service errors.
        """
        logger.info(f"Received GET request for location: {location}")

        if not location or not isinstance(location, str) or location.strip() == "":
             logger.warning(f"Received invalid location input: {location}")
             return Response(
                 {"error": "Invalid location provided. Location cannot be empty."},
                 status=status.HTTP_400_BAD_REQUEST
             )

        cache_key = f"weather_data:{location.lower().strip().replace(' ', '_')}"
        logger.debug(f"Checking cache for key: {cache_key}")

        cached_data = cache.get(cache_key)

        if cached_data:
            logger.info(f"Cache hit for location: {location}")
            return Response(cached_data)
        else:
            logger.info(f"Cache miss for location: {location}. Attempting to fetch from API...")

            try:
                weather_data = get_weather_data(location)

                logger.info(f"Successfully fetched weather data for {location} from API.")

                cache_timeout = 60 * 60 * 12 # 12 hours
                cache.set(cache_key, weather_data, timeout=cache_timeout)
                logger.info(f"Cached data for {location} with timeout {cache_timeout} seconds.")

                return Response(weather_data, status=status.HTTP_200_OK)

            except WeatherServiceAPIError as e:
                logger.error(f"Weather API error for {location}: Status {e.status_code}, Message: {e.message}")
                if e.status_code == 404:
                     return Response(
                         {"error": f"Location '{location}' not found by external weather service."},
                         status=status.HTTP_404_NOT_FOUND
                     )
                return Response(
                    {"error": f"External weather API error: {e.message}", "api_details": e.api_response},
                    status=status.HTTP_502_BAD_GATEWAY
                )
            except WeatherServiceTimeoutError as e:
                 logger.error(f"Weather API timeout for {location}: {e}")
                 return Response(
                     {"error": "External weather service request timed out."},
                     status=status.HTTP_504_GATEWAY_TIMEOUT
                 )
            except WeatherServiceConnectionError as e:
                logger.error(f"Weather API connection error for {location}: {e}")
                return Response(
                    {"error": "Could not connect to external weather service."},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
            except WeatherServiceError as e:
                logger.error(f"Weather service error for {location}: {e}")
                return Response(
                    {"error": f"An error occurred in the weather service: {e}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            except Exception as e:
                logger.error(f"An unexpected error occurred in weather view for {location}: {e}", exc_info=True)
                return Response(
                    {"error": "An unexpected server error occurred."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
