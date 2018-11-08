from django.shortcuts import render
from crickets.models import *
from django.db.models import Count, Sum, Q
from django.views import generic
from django.forms import ModelForm
from django.http import HttpResponseRedirect, HttpResponse
import datetime

# Create your views here.

def holding(request):
    return render(request, 'crickets/holding.html', {})

def index(request):
    # on installation version - clear the session stuff here...
    #request.session.flush()
    context={}
    context['done_training'] = False
    # don't add anything to session till player has passed check
    if 'done_training' in request.session:
        print(request.session["done_training"])
        context['done_training'] = request.session["done_training"]
        
    return render(request, 'crickets/index.html', context)

def about(request):
    return render(request, 'crickets/about.html', {})

def check(request):
    return render(request, 'crickets/check.html', {})

def training(request):
    return render(request, 'crickets/training.html', {})

def choose(request):
    # can only have got here via training or already done with check passed...

    request.session["done_training"]=True

    if 'player_number' not in request.session:
        player = Player(name = "???", videos_watched = 0)
        player.save()
        request.session["player_number"]=player.id

    context = {}
    context['crickets'] = Cricket.objects.exclude(videos_ready__lt=5).order_by('activity')[:5]
    return render(request, 'crickets/choose.html', context)

class CricketView(generic.DetailView):
    model = Cricket
    template_name = 'crickets/play.html'
    def get_context_data(self, **kwargs):
        context = super(CricketView, self).get_context_data(**kwargs)
        # just a random movie for the moment...
        context['movies'] = Movie.objects.filter(cricket=context['cricket']).exclude(status=0).order_by('?')[:5]
        context['path'] = str(context['movies'][0].season)+"/"+context['movies'][0].camera

        # check using the session to see where we need to go
        # after this - keyboard or personality
        context['done_keyboard']=False
        context['player_number']=-1
        if 'player_number' in self.request.session:
            player = Player.objects.get(pk=self.request.session["player_number"])
            context["player_id"]=self.request.session["player_number"]
            if player.name != "???":
                context['done_keyboard']=True

        return context 

def avg_time(datetimes):
    total = sum(dt.hour * 3600 + dt.minute * 60 + dt.second for dt in datetimes)
    return total / len(datetimes)

def score(score, min_score, max_score):
    ret = ((score-min_score)/(max_score-min_score))*100
    if ret>100: return 100
    if ret<0: return 0
    return ret

class PersonalityView(generic.DetailView):
    model = Cricket
    template_name = 'crickets/personality.html'
    def get_context_data(self, **kwargs):
        context = super(PersonalityView, self).get_context_data(**kwargs)
        # need to calculate the cricket data *here* as 
        # these need to include the player's data just
        # saved - not rely on the robot update
        cricket = context['cricket']
        context['eating_score'] = score(Event.objects.filter(movie__cricket=cricket,event_type='eating').count(),
                                        Value.objects.filter(name='eating_min')[0].value,
                                        Value.objects.filter(name='eating_max')[0].value)
        context['singing_score'] = score(Event.objects.filter(movie__cricket=cricket,event_type='singing').count(),
                                         Value.objects.filter(name='singing_min')[0].value,
                                         Value.objects.filter(name='singing_max')[0].value)
        context['moving_score'] = score(Event.objects.filter(movie__cricket=cricket).filter(Q(event_type="in")|Q(event_type="mid")|Q(event_type="out")).count(),
                                        Value.objects.filter(name='moving_min')[0].value,
                                        Value.objects.filter(name='moving_max')[0].value)
        
        # keeping cricket.daynight_score just in case this
        # becomes too slow...
        times = []
        for event in Event.objects.filter(movie__cricket=cricket):
            times.append(event.estimated_real_time)
        if len(times)>0:
            a = avg_time(times)
            context['daynight_score']=(a/(60.0*60.0*24))*100

        return context 

class ResultsMovementView(generic.DetailView):
    model = Cricket
    template_name = 'crickets/results_movement.html'
    def get_context_data(self, **kwargs):
        context = super(ResultsMovementView, self).get_context_data(**kwargs)
        cricket = context['cricket']

        times = []
        for event in Event.objects.filter(movie__cricket=cricket).filter(Q(event_type="in")|Q(event_type="mid")|Q(event_type="out")):
            times.append(event.estimated_real_time)
        if len(times)>0:
            a = avg_time(times)
            context['moving_score']=(a/(60.0*60.0*24))*100
        else:
            context['moving_score']=0

        return context 

class ResultsEatingView(generic.DetailView):
    model = Cricket
    template_name = 'crickets/results_eating.html'
    def get_context_data(self, **kwargs):
        context = super(ResultsEatingView, self).get_context_data(**kwargs)
        cricket = context['cricket']
        
        times = []
        for event in Event.objects.filter(movie__cricket=cricket,event_type="eating"):
            times.append(event.estimated_real_time)
        if len(times)>0:
            a = avg_time(times)
            context['eating_score']=(a/(60.0*60.0*24))*100
        else:
            context['eating_score']=0

        return context 

class ResultsSingingView(generic.DetailView):
    model = Cricket
    template_name = 'crickets/results_singing.html'
    def get_context_data(self, **kwargs):
        context = super(ResultsSingingView, self).get_context_data(**kwargs)
        cricket = context['cricket']

        times = []
        for event in Event.objects.filter(movie__cricket=cricket,event_type="singing"):
            times.append(event.estimated_real_time)
        if len(times)>0:
            a = avg_time(times)
            context['singing_score']=(a/(60.0*60.0*24))*100
        else:
            context['singing_score']=0

        return context 

class KeyboardView(generic.DetailView):
    model = Cricket
    template_name = 'crickets/keyboard.html'
    def get_context_data(self, **kwargs):
        context = super(KeyboardView, self).get_context_data(**kwargs)
        
        context['num_videos']=0
        if 'player_number' in self.request.session:
            player = Player.objects.get(pk=self.request.session["player_number"])
            context['num_videos']=player.videos_watched
            context["player_id"]=player.id

        return context 

def player_name(request):
    if request.method == 'POST':
        if 'player_number' in request.session:
            player = Player.objects.get(pk=request.session["player_number"])
            player.name=request.POST['name'][:3]
            player.save()
    return HttpResponse('')

class LeaderboardView(generic.DetailView):
    model = Cricket
    template_name = 'crickets/leaderboard.html'
    def get_context_data(self, **kwargs):
        context = super(LeaderboardView, self).get_context_data(**kwargs)
        context["player_list"]=Player.objects.exclude(name="???").exclude(videos_watched=0).order_by('-videos_watched')[:20]
        return context

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

            obj = Event() #gets new object
            obj.movie = form.cleaned_data['movie']
            obj.event_type = form.cleaned_data['event_type']
            obj.user = form.cleaned_data['user']
            obj.video_time = form.cleaned_data['video_time']
            obj.x_pos = form.cleaned_data['x_pos']
            obj.y_pos = form.cleaned_data['y_pos']
            obj.other = form.cleaned_data['other']

            # calculate dodgy time estimation based on proportion
            # through screen video and move start/end time            
            movie = obj.movie            
            screen_length_secs = 30
            t = obj.video_time/screen_length_secs
            diff = movie.end_time-movie.start_time            
            realtime = movie.start_time+datetime.timedelta(seconds=diff.total_seconds()*t)
            obj.save()
            # for some reason need to re-save this
            obj.estimated_real_time = realtime
            obj.save()
            
            # get the the cricket 
            cricket = Cricket.objects.get(pk=movie.cricket.id)            
                
            if obj.event_type=="burrow_start":
                cricket.activity+=1
                movie.views+=1
                movie.save()

            if obj.event_type=="cricket_end" or obj.event_type=="no_cricket_end":
                # on burrow_start update player videos watched
                if "player_number" in request.session:
                    player = Player.objects.get(pk=request.session["player_number"])
                    player.videos_watched+=1
                    player.save()
                
            cricket.save()
            return HttpResponse('')
        print(form.errors)
        return HttpResponse('request is invalid: '+str(form))
    else:
        form = EventForm()
        return render(request, 'crickets/event.html', {'form': form})
