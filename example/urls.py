from django.conf.urls.defaults import patterns, include, url

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import views

from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
        url(r'^$', direct_to_template, name='index', kwargs={"template": 'index.html'}),
        url(r'^example_1/$', views.example_1, name='example_1'),
        url(r'^example_2/$', views.example_2, name='example_2'),
)

urlpatterns += staticfiles_urlpatterns()
