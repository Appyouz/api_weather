import logging
from asyncio import exceptions

import requests
from django.conf import settings

logger = logging.getLogger(__name__)
VISUAL_CROSSING_BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"

def get_weather_data(location):
    api_key = settings.VISUAL_CROSSING_API_KEY

    params = {
        'key': api_key,
        'unitGroup': 'metric',
        'include': 'days',
    }

    url = f"{VISUAL_CROSSING_BASE_URL}{location}"
    
    logger.info(f"Attempting to fetch weather data for location: {location}")

    try:
        response = requests.get(url,params=params, timeout=10)
        
        response.raise_for_status()

        weather_data = response.json()

        logger.info(f"Successfully fetched weather data for location: {location}")

        return weather_data

    except requests.exceptions.Timeout:
        logger.error(f"Request timed out while fetching weather for {location}")
        return None
    except requests.exceptions.ConnectionError:
        logger.error(f"Connection Error while fetchin weather for {location}. Is the API reachable?")
        return None
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred while fetching weather for {location}: {e}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred during the API request for {location}: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occured: {e}", exc_info=True)
        return None
