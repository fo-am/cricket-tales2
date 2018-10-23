from django.shortcuts import render
from crickets.models import *
from django.db.models import Count, Sum
from django.views import generic

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
    context = {}
    context['crickets'] = Cricket.objects.exclude(videos_ready=0).order_by('?')
    return render(request, 'crickets/choose.html', context)

class CricketView(generic.DetailView):
    model = Cricket
    template_name = 'crickets/play.html'
    def get_context_data(self, **kwargs):
        context = super(CricketView, self).get_context_data(**kwargs)
        # just a random movie for the moment...
        context['movie'] = Movie.objects.filter(cricket=context['cricket']).exclude(status=0).order_by('?')[1]
        context['path'] = str(context['movie'].season)+"/"+context['movie'].camera
        return context 

def keyboard(request):
    return render(request, 'crickets/keyboard.html', {})
