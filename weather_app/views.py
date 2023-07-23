from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import CitySearchHistorySerializer
from .models import TaskLog, CitySearchHistory
from .tasks import fetch_weather_data
from datetime import datetime
from django.utils import timezone

class UserSearchHistoryView(generics.ListAPIView):
    serializer_class = CitySearchHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return CitySearchHistory.objects.filter(user_id=user_id)

@api_view(['POST'])
def create_task(request):
    city_name = request.data.get('city')
    country_name = request.data.get('country')
    scheduled_datetime_str = request.data.get('schedule')
    scheduled_datetime = datetime.strptime(scheduled_datetime_str, '%Y-%m-%dT%H:%M:%SZ')
    scheduled_datetime = timezone.make_aware(scheduled_datetime)
    print("DBUG celery", city_name, country_name, scheduled_datetime, type(scheduled_datetime))

    # Save the task in the TaskLog model
    task_log = TaskLog.objects.create(city_name=city_name, country_name=country_name, scheduled_datetime=scheduled_datetime)

    # Schedule the task using Celery
    fetch_weather_data.apply_async(args=[city_name,country_name], eta=scheduled_datetime)

    return Response({"message": "Task created successfully!", "task_id": task_log.id})

@api_view(['GET'])
def task_history(request):
    # Retrieve the task history from the TaskLog model
    task_history = TaskLog.objects.all()
    data = [{"id": task.id, "city_name": task.city_name, "scheduled_datetime": task.scheduled_datetime,
             "status": task.status, "time_of_creation": task.time_of_creation,
             "time_of_completion": task.time_of_completion} for task in task_history]
    
    return Response(data)

@api_view(['GET'])
def get_weather_data(request):
    city_name = request.query_params.get('city')
    country_name = request.query_params.get('country')
    print(city_name, request, request.user.id)
    if not city_name:
        return Response({'error': 'City name is required.'}, status=400)

    api_key = '77b7d4fa2f6b05ab97b39c227bba2ff3'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'

    try:
        response = requests.get(url)
        data = response.json()
        data['country'] = country_name
        search_data = {
            'city_name': city_name,
            'country_name': country_name,
            'user': request.user.id,
        }
        serializer = CitySearchHistorySerializer(data=search_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data)
    except requests.exceptions.RequestException as e:
        return Response({'error': 'Failed to fetch data from the API.'}, status=500)
    
@api_view(['GET'])
def get_city_suggestions(request):
    city_name = request.query_params.get('city')
    print(city_name, request)
    if not city_name:
        return Response({'error': 'City name is required.'}, status=400)
    
    limit = 10
    if len(city_name) <= 2:
        limit = 10
    elif len(city_name) > 2 and len(city_name) <= 5:
        limit = 4
    else:
        limit = 1

    url = f'http://api.geonames.org/searchJSON?q={city_name}&name_startsWith={city_name}&maxRows={limit}&username=haris'

    try:
        response = requests.get(url)

        data = response.json()

        city_country_pairs = []
        # Create a set to store unique city-country pairs
        city_country_set = set()

        # Extract city names from the API response and create city-country pairs
        for result in data['geonames']:
            city_name = result['name']
            country_name = result['countryName']

            # Append the city-country pair to the set (as tuples)
            city_country_set.add((city_name, country_name))

        # Convert the set back to a list of dictionaries
        city_country_pairs = [{'city': city, 'country': country} for city, country in city_country_set]
        return Response(city_country_pairs)
    except requests.exceptions.RequestException as e:
        return Response({'error': 'Failed to fetch data from the API.'}, status=500)