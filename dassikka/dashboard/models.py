from django.db import models
# Create your models here.
class busscheduletable(models.Model):
    line = models.CharField(max_length=10)
    time = models.CharField(max_length=10)
    loadtime = models.CharField(max_length=50)

    class Meta:
        db_table = 'bus_schedule_table'


class headlinetable(models.Model):
    headline = models.CharField(max_length=255)
    loadtime = models.CharField(max_length=50)

    class Meta:
        db_table = 'headline_table'


class weathertable(models.Model):
    temperature = models.DecimalField(decimal_places=2, max_digits=5)
    rf_temperature = models.DecimalField(decimal_places=2, max_digits=5)
    icon_code = models.CharField(max_length=10)
    weather_type = models.CharField(max_length=50)
    forecast_type = models.CharField(max_length=15)
    loadtime = models.CharField(max_length=50)

    class Meta:
        db_table = 'weather_table'
        get_latest_by = '-loadtime'

class sensehattable(models.Model):
    temperature = models.DecimalField(decimal_places=2, max_digits=5)
    humidity = models.DecimalField(decimal_places=2, max_digits=5)
    measuretime = models.CharField(max_length=20)
    loadtime = models.CharField(max_length=17)

    class Meta:
        db_table = 'sense_hat_table'
