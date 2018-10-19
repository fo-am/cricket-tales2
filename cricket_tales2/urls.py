from django.conf.urls import patterns, include, url
from django.contrib import admin
from crickets import views

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
)

urlpatterns += patterns('',
       (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
