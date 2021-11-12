from django.shortcuts import render
from .models import Station

# Create your views here.
def home(request):
    stations = Station.objects.all()
    context = {'stations': stations}
    return render(request, 'home.html', context)
         #       # nome do template  # contexto  
