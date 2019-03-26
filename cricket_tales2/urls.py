from django.conf.urls import patterns, include, url
from django.contrib import admin
from crickets import views
from django.views.decorators.csrf import csrf_exempt

import settings

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^beta/', views.index, name='index'),
    url(r'^exhib/', views.index_exhib, name='exhib'),
    url(r'^admin/', include(admin.site.urls)),
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
    url(r'^player_name/', views.player_name, name='player_name'),
    url(r'^leaderboard/(?P<pk>\d+)/', views.LeaderboardView.as_view(), name='leaderboard'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)

urlpatterns += patterns('',
       (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
