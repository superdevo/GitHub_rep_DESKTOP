from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/books/report/$','books.admin_views.report'),
    url(r'^admin/books/book/add/$','books.admin_views.add_by_isbn'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^app1/', include('app1.urls'),name='app1'),
    url(r'^books/', include('books.urls'), name="books")
)
