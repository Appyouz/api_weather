import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

class WeatherServiceError(Exception):
    """Base exception for weather service errors."""
    pass

class WeatherServiceTimeoutError(WeatherServiceError):
    """Raised when the weather API request times out."""
    pass

class WeatherServiceConnectionError(WeatherServiceError):
    """Raised when there's a connection issue with the weather API."""
    pass

class WeatherServiceAPIError(WeatherServiceError):
    """Raised for non-200 HTTP responses from the weather API."""
    def __init__(self, status_code, message=None, api_response=None):
        self.status_code = status_code
        self.message = message or f"API returned status code {status_code}"
        self.api_response = api_response
        super().__init__(self.message)


VISUAL_CROSSING_BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"

def get_weather_data(location):
    """
    Fetches weather data for a given location from the Visual Crossing API.

    Args:
        location (str): The location (e.g., city name, city,state,country).

    Returns:
        dict: A dictionary containing weather data if the request is successful.

    Raises:
        WeatherServiceTimeoutError: If the request times out.
        WeatherServiceConnectionError: If a connection error occurs.
        WeatherServiceAPIError: If the API returns a non-200 status code.
        WeatherServiceError: For other unexpected request exceptions.
    """
    api_key = settings.VISUAL_CROSSING_API_KEY

    params = {
        'key': api_key,
        'unitGroup': 'metric',
        'include': 'days',
    }

    url = f"{VISUAL_CROSSING_BASE_URL}{location}"

    logger.info(f"Attempting to fetch weather data for location: {location}")

    try:
        response = requests.get(url, params=params, timeout=10)

        if not response.status_code == 200:
            api_error_details = None
            try:
                api_error_details = response.json()
            except requests.exceptions.JSONDecodeError:
                pass # Ignore if response is not JSON

            raise WeatherServiceAPIError(
                status_code=response.status_code,
                message=f"API returned non-200 status code: {response.status_code}",
                api_response=api_error_details
            )

        weather_data = response.json()

        logger.info(f"Successfully fetched weather data for location: {location}")
        return weather_data

    except requests.exceptions.Timeout:
        logger.error(f"Request timed out while fetching weather for {location}")
        raise WeatherServiceTimeoutError(f"Weather API request timed out for {location}")
    except requests.exceptions.ConnectionError:
        logger.error(f"Connection error while fetching weather for {location}. Is the API reachable?")
        raise WeatherServiceConnectionError(f"Connection error to weather API for {location}")
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred during the API request for {location}: {e}")
        raise WeatherServiceError(f"An unexpected API request error occurred for {location}: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred in weather service: {e}", exc_info=True)
        raise WeatherServiceError(f"An unexpected error occurred: {e}")
