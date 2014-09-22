from django.conf.urls import patterns, url
from comm import views

urlpatterns = patterns('', 
	url(r'^(?P<country>[\w+ ]+)/(?P<state>[\w+ ]+)/(?P<city>[\w+ ]+)/$', views.comm_place, name='comm_place'),
	url(r'^post/(?P<post_id>[0-9]+)/$', views.post_details, name='post_details'),
	url(r'^post/register/$', views.create_post, name='create_post'),
	url(r'^post/success/$',views.post_saved, name='post_saved'),
	url(r'^post/rate/$', views.post_rate, name='post_rate'),
)