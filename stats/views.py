from django.shortcuts import render, redirect, get_object_or_404
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