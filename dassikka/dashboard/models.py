from django.db import models
# Create your models here.
class busscheduletable(models.Model):
    line = models.CharField(max_length=10)
    time = models.CharField(max_length=10)
    loadtime = models.CharField(max_length=50)

    class Meta:
        db_table = 'busscheduletable'


class headlinetable(models.Model):
    headline = models.CharField(max_length=255)
    loadtime = models.CharField(max_length=50)

    class Meta:
        db_table = 'headlinetable'


class weathertable(models.Model):
    temperature = models.CharField(max_length=10)
    rf_temperature = models.CharField(max_length=10)
    icon_code = models.CharField(max_length=10)
    weather_type = models.CharField(max_length=50)
    forecast_type = models.CharField(max_length=8)
    loadtime = models.CharField(max_length=50)

    class Meta:
        db_table = 'weathertable'
