from django.conf.urls import patterns, include, url
from home import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^browse/', include('browse.urls'), name='browse'),
    url(r'^home/', include('home.urls'), name='home'),
    url(r'^comm/', include('comm.urls'), name='comm'),
    #include('home.urls')
)