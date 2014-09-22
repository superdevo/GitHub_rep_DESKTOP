from django.conf.urls import url, patterns
from django.views.generic import TemplateView 
from books import views

#<<--- calling a template WITHOUT writing a VIEW!!!!!

urlpatterns = patterns('',
	url(r'^$', views.IndexView.as_view(paginate_by=3), name='index'),
	url(r'^search/$', views.search),
	url(r'^contact/$', views.contact),
	url(r'^contact/thanks/$', TemplateView.as_view(template_name='thankyou.html')),
	url(r'^add_publisher/thanks/$', TemplateView.as_view(template_name='thankyou-publisher.html')),
	url(r'^add_publisher/$', views.add_publisher),
	url(r'^authors/$', views.show_authors),
	url(r'^image-from-raw-data/$', views.load_image),
)