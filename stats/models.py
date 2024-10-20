from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
class Plot(models.Model):
    name = models.CharField(max_length=100)
    plant = models.CharField(max_length=100)
    plot = models.ImageField(upload_to='plots/')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('stats:dashboard', kwargs={'name': self.name})

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.plant:
            self.plant = 'Unassigned'
        super(Plot, self).save(*args, **kwargs)
class PerfectStats(models.Model):
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE)
    light = models.FloatField()
    ambientTemperature = models.FloatField()
    ambientHumidity = models.FloatField()
    soilMoistur = models.FloatField()
    soilTemperature = models.FloatField()
    soilPh = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.plot.name

class RealStats(models.Model): 
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE)
    light = models.FloatField()
    ambientTemperature = models.FloatField()
    ambientHumidity = models.FloatField()
    soilMoistur = models.FloatField()
    soilTemperature = models.FloatField()
    soilPh = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.plot.name
    
    def save(self, *args, **kwargs):
        super(RealStats, self).save(*args, **kwargs)
        self.plot.save()

class Tank(models.Model):
    name = models.CharField(max_length=100)
    volume = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name