# Weather Bridge API Service

This project is a backend service built with Django that acts as a wrapper around a third-party Weather API (Visual Crossing). It fetches weather data for a given location and implements a caching layer using Redis to improve performance and reduce calls to the external API.

This project was built as part of my backend learning journey, following project ideas from [roadmap.sh/backend/project-ideas](https://roadmap.sh/backend/project-ideas).

## Features

* Integrates with the Visual Crossing Weather API to fetch current and forecast weather data.
* Implements a Redis caching strategy to store weather data for specific locations.
* Serves cached data for repeat requests within a defined timeout period, falling back to the external API on a cache miss or cache expiration.
* Provides a RESTful API endpoint using Django REST Framework.
* Includes basic input validation and structured error handling for API calls and service communication.

## Technologies Used

* **Backend Framework:** Django
* **API Development:** Django REST Framework (DRF)
* **Database:** MySQL (Configured, though not extensively used for core weather/caching logic in this project)
* **Caching:** Redis
* **External API Calls:** Python `requests` library
* **Environment Variables:** `python-dotenv`
* **Other:**
    * `asgiref`
    * `certifi`
    * `charset-normalizer`
    * `django-redis`
    * `django-stubs`, `django-stubs-ext`, `types-PyYAML`, `typing_extensions` (for type checking)
    * `idna`
    * `mysqlclient`
    * `sqlparse`
    * `urllib3`

## Setup and Installation

1.  **Clone the Repository:**
    ```bash
    git clone git@github.com:Appyouz/api_weather.git
    cd weather_bridge 
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment:**
    * On Windows: `venv\Scripts\activate`
    * On macOS/Linux: `source venv/bin/activate`

4.  **Install Dependencies:**
    Install the required Python packages using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set up Environment Variables:**
    Create a `.env` file in the project root directory (where `manage.py` is located). Add your Visual Crossing API key:
    ```env
    VISUAL_CROSSING_API_KEY='your_visual_crossing_api_key_here'
    # Add other sensitive settings here if needed
    ```
    Replace `'your_visual_crossing_api_key_here'` with your actual API key obtained from Visual Crossing.

6.  **Set up Redis:**
    Ensure you have a Redis server installed and running. The project is configured to connect to Redis at `redis://127.0.0.1:6379/1` by default (as per `settings.py`). If your Redis is elsewhere, update the `CACHES` setting in `weather_bridge/settings.py`.

7.  **Apply Database Migrations:**
    Although this project doesn't use models extensively, it's good practice to apply default migrations:
    ```bash
    python manage.py migrate
    ```

## How to Run

1.  Make sure your virtual environment is activated.
2.  Make sure your Redis server is running.
3.  Navigate to the project root directory (where `manage.py` is located).
4.  Run the Django development server:
    ```bash
    python manage.py runserver
    ```
    The server will start, typically at `http://127.0.0.1:8000/`.

## API Endpoint Usage

The weather data is available via a GET request to the following endpoint:
