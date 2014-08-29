from django.conf.urls import url, patterns
from usertrial import views
from django.contrib.auth.views import login, logout
#<<--- calling a template WITHOUT writing a VIEW!!!!!

urlpatterns = patterns('',
	url(r'^$', views.load_template, {'which_view' : 'index.html'}),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', login),
	url(r'^logout/$', logout, {'template_name': 'logged_out.html'}),
	url(r'^profile/$', views.load_template, {'which_view' : 'profile.html'}),
	url(r'^get-csv/$', views.unruly_passengers_csv, name='unruly_passengers_csv'),
	url(r'^get-pdf/$', views.get_pdf, name='get_pdf'),
	url(r'^get-complex-pdf/$', views.get_complex_pdf, name='get_complex_pdf'),
	url(r'^set-favorite-color/$', views.set_color, name='favorite_color'),
	url(r'^show-color/$', views.show_color, name='show_color'),
	url(r'^restricted/$', views.restricted_zone, name='restricted_zone'),
)
