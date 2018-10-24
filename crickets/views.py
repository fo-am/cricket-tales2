from django.shortcuts import render
from crickets.models import *
from django.db.models import Count, Sum
from django.views import generic
from django.forms import ModelForm
from django.http import HttpResponseRedirect, HttpResponse
import datetime

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
    context['crickets'] = Cricket.objects.exclude(videos_ready=0).order_by('activity')[:5]
    return render(request, 'crickets/choose.html', context)

class CricketView(generic.DetailView):
    model = Cricket
    template_name = 'crickets/play.html'
    def get_context_data(self, **kwargs):
        context = super(CricketView, self).get_context_data(**kwargs)
        # just a random movie for the moment...
        context['movies'] = Movie.objects.filter(cricket=context['cricket']).exclude(status=0).order_by('?')[:5]
        context['path'] = str(context['movies'][0].season)+"/"+context['movies'][0].camera
        return context 

def keyboard(request):
    return render(request, 'crickets/keyboard.html', {})

class EventForm(ModelForm):
     class Meta:
         model = Event
         fields = "__all__"

## incoming from javascript...
def record_event(request):
    if request.method == 'POST':
        # concerned about how much overhead is involved
        # with this, as it's generating an option list entry
        # for each movie - seen when you print (but perhaps they
        # are not actually created until printing)
        form = EventForm(request.POST)
        # probably not even needed, but who knows where these may
        # be coming from eventually...?

        if form.is_valid():
            form.save()
            data = form.cleaned_data
            movie = data["movie"]
            # get the the cricket 
            cricket = Cricket.objects.get(pk=movie.cricket.id)
            
            # daynight_score?
            if movie.start_time.time()<datetime.time(6,0,0) or \
               movie.start_time.time()>datetime.time(18,0,0):
                print("nighttime")
                if data["event_type"]=="eating": cricket.eating_score+=1
                if data["event_type"]=="singing": cricket.singing_score+=1
                if data["event_type"]=="in": cricket.moving_score+=1
                if data["event_type"]=="mid": cricket.moving_score+=1
                if data["event_type"]=="out": cricket.moving_score+=1
            else:
                print("daytime")
                if data["event_type"]=="eating": cricket.eating_score+=1
                if data["event_type"]=="singing": cricket.singing_score+=1
                if data["event_type"]=="in": cricket.moving_score+=1
                if data["event_type"]=="mid": cricket.moving_score+=1
                if data["event_type"]=="out": cricket.moving_score+=1
                
            if data["event_type"]=="burrow_start":
                # on burrow_start update player videos watched
                cricket.activity+=1
                movie.views+=1
                movie.save()

            cricket.save()

            # # if we're not anonymous
            # if data["user"]:
            #     profile = data["user"].profile
            #     profile.num_events+=1
            #     profile.save()

            #     user = data["user"]
            #     movie = data["movie"]

            #     # update the score for this user if it's the last
            #     # event (we can also calculate these by counting the
            #     # cricket end's in the event table if we need to)
            #     if data["type"].name == "Cricket End":
            #         update_score(user,movie.burrow)

            #     update_stories(user,data)
            return HttpResponse('')
        return HttpResponse('request is invalid: '+str(form))
    else:
        form = EventForm()
        return render(request, 'crickets/event.html', {'form': form})
