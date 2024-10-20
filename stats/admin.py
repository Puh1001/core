from django.contrib import admin
from .models import Plot, PerfectStats,RealStats, Tank

# Register your models here.
admin.site.register(Plot)
admin.site.register(PerfectStats)
admin.site.register(Tank)
admin.site.register(RealStats)