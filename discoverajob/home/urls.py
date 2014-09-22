from django.conf.urls import patterns, url
from home import views

urlpatterns = patterns('', 
	url(r'^$', views.home, name='home'),
	url(r'^accounts/register/$', views.register_user, name='register_user'),
	url(r'^accounts/login/$', views.login_user, name='login_user'),
	url(r'^accounts/logout/$', views.logout_user, name='logout_user'),
	url(r'^accounts/profile/(?P<profile_id>[0-9]+)/$', views.load_profile, name='load_profile'),
)