from django.conf.urls import patterns, url
from django.conf.urls import include

from crickets import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)
