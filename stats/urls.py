from django.urls import path
from .views import index, dashboard

app_name = 'stats'

urlpatterns = [
    path('', index, name='index'),
    path('<name>', dashboard, name='dashboard'),
]