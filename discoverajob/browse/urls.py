from django.conf.urls import patterns, url
from browse import views

urlpatterns = patterns('',
		url(r'^geo/$', views.load_geo, name='load_geo'),
		url(r'^geo/states/$', views.ajax_states, name='ajax_states'),
		url(r'^geo/cities/$', views.ajax_cities, name='ajax_cities'),
		url(r'^geo/preview/$', views.ajax_preview, name='ajax_preview'),
	)