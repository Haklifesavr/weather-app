from django.db import models
from django.contrib.auth import get_user_model

class CitySearchHistory(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    city_name = models.CharField(max_length=255)
    country_name = models.CharField(max_length=255)
    search_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.city_name} - {self.search_date}"
