from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Plot, PerfectStats, RealStats, Tank
from faker import Faker
# Create your views here.

fake = Faker()

def index(request):
    plots = Plot.objects.all()
    if request.method == 'POST':
        newPlot = request.POST.get('newPlot');
        obj, _ = Plot.objects.get_or_create(name=newPlot)
        print(obj)
        return redirect('stats:dashboard', obj.name)
    return render(request, 'index.html', {'plots': plots})

def dashboard(request, name):
    obj = get_object_or_404(Plot, name=name)
    return render(request, 'dashboard.html', {'name': obj.name if obj.name else fake.name(), 'plant': obj.plant})

def get_tanks(request):
    tanks = Tank.objects.all().values('id', 'name', 'volume')
    return JsonResponse(list(tanks), safe=False)

@csrf_exempt
def control_tank(request):
    if request.method == 'POST':
        tank_id = request.POST.get('tank_id')
        action = request.POST.get('action') 
        try:
            tank = Tank.objects.get(id=tank_id)
            return JsonResponse({'status': 'success', 'action': action, 'tank': tank.name})
        except Tank.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Tank not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})