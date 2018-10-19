from django.shortcuts import render
from crickets.models import *
from django.db.models import Count, Sum

# Create your views here.

def index(request):
    context = {}
    context['hide_menu'] = True
    context['num_videos_watched'] = Movie.objects.all().aggregate(Sum('views'))['views__sum']
    context['num_events'] = Event.objects.all().count()
    context['num_videos'] = Movie.objects.all().count()
    return render(request, 'crickets/index.html', context)

def about(request):
    return render(request, 'crickets/about.html', {})

def check(request):
    return render(request, 'crickets/check.html', {})

def training(request):
    return render(request, 'crickets/training.html', {})

def choose(request):
    return render(request, 'crickets/choose.html', {})

def play(request):
    return render(request, 'crickets/play.html', {})

def keyboard(request):
    return render(request, 'crickets/keyboard.html', {})
