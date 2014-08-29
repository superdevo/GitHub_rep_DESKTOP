from django.conf.urls import url
from devomag import views

urlpatterns = [
	#index view at /devomag/
	url(r'^$', views.IndexView.as_view(), name='index'),
	#VIEW FOR THANKYOU AFTER SUBMISSION
	url(r'^submit-new-article/thanks/$', views.thankyou, name='thankyou'),
	#detail view at /devomag/*BLOG-ENTRY*/
	url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
	#detail view for author at/devomag/author/*ID*
	url(r'^(?P<pk>[0-9]+)/author/$', views.AuthDetailsView.as_view(), name='auth_details'),
	#url for new article submission
	url(r'^submit-new-article/$', views.NewArticle, name='newarticle')
	]
#views.NOMEDELLATUAVISTA!!, that is the same in name parameter
