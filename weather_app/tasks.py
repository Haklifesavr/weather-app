# tasks.py

from celery import shared_task, Celery
from django.utils import timezone
from weather_app.models import TaskLog
import requests

# celery_app = Celery('weather_app')
# celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# @celery_app.task
@shared_task
def fetch_weather_data(city_name, country_name):
    # Fetch weather data from the API using city_name
    # Replace 'your_api_key' with your actual OpenWeatherMap API key
    api_key = '77b7d4fa2f6b05ab97b39c227bba2ff3'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
    response = requests.get(url)
    weather_data = response.json()

    print("DEBUG CELERY WEATHER DATA", weather_data)

    # Save the weather data to your database or update the TaskLog model
    # Example code: (you may need to modify this based on your models)
    task_log = TaskLog.objects.get(city_name=city_name, country_name=country_name)
    task_log.status = 'done'
    task_log.time_of_completion = timezone.now()
    task_log.save()

    # Process and store the weather data as needed
    # ...

    return "Weather data fetched and processed successfully!"
