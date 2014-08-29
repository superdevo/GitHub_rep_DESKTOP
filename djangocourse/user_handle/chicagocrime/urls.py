from django.conf.urls import patterns, url
from chicagocrime import views
from chicagocrime.feeds import LatestEntriesFeed

urlpatterns = patterns('', 
	url(r'^$', views.index, name='index'),
	url(r'^latest/feed/$', LatestEntriesFeed()),
	url(r'^news-item/(?P<item>[0-9]+)/$', views.news_item, name='news-item'),
	)