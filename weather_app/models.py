from django.db import models
from django.contrib.auth import get_user_model

class TaskLog(models.Model):
    city_name = models.CharField(max_length=255)
    country_name = models.CharField(max_length=255)
    scheduled_datetime = models.DateTimeField()
    status_choices = (
        ('initiated', 'Initiated'),
        ('done', 'Done'),
    )
    status = models.CharField(max_length=10, choices=status_choices, default='initiated')
    time_of_creation = models.DateTimeField(auto_now_add=True)
    time_of_completion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.city_name} - {self.scheduled_datetime} - {self.status}"

class CitySearchHistory(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    city_name = models.CharField(max_length=255)
    country_name = models.CharField(max_length=255)
    search_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.city_name} - {self.search_date}"
