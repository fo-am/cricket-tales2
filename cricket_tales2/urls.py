from django.conf.urls import patterns, include, url
from django.contrib import admin
from crickets import views
from django.views.decorators.csrf import csrf_exempt

import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cricket_tales2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^check/', views.check, name='check'),
    url(r'^training/', views.training, name='training'),
    url(r'^choose/', views.choose, name='choose'),
    url(r'^play/(?P<pk>\d+)/$', views.CricketView.as_view(), name='play'),
    url(r'^keyboard/(?P<pk>\d+)/$', views.KeyboardView.as_view(), name='keyboard'),
    url(r'^event/', views.record_event, name='event'),
    url(r'^personality/(?P<pk>\d+)/$', views.PersonalityView.as_view(), name='personality'),
    url(r'^results_movement/(?P<pk>\d+)/$', views.ResultsMovementView.as_view(), name='results_movement'),
    url(r'^results_eating/(?P<pk>\d+)/$', views.ResultsEatingView.as_view(), name='results_eating'),
    url(r'^results_singing/(?P<pk>\d+)/$', views.ResultsSingingView.as_view(), name='results_singing'),
    url(r'^player_name/', csrf_exempt(views.player_name), name='player_name'),
    url(r'^leaderboard/(?P<pk>\d+)/', views.LeaderboardView.as_view(), name='leaderboard'),
)

urlpatterns += patterns('',
       (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
