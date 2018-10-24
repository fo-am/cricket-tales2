from django.shortcuts import render
from crickets.models import *
from django.db.models import Count, Sum
from django.views import generic
from django.forms import ModelForm
from django.http import HttpResponseRedirect, HttpResponse

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
        print(form)
        if form.is_valid():
            form.save()
            # update the stats for this player
            # too much here???
            # either this or a laggy continual robot.py process
            #data = form.cleaned_data

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
