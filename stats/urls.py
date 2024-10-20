from django.urls import path
from . import views

app_name = 'stats'

urlpatterns = [
    path('', views.index, name='index'),
    path('<name>', views.dashboard, name='dashboard'),
    path('get-tanks/', views.get_tanks, name='get_tanks'),
    path('control-tank/', views.control_tank, name='control_tank'),
    # Các URL khác...
]