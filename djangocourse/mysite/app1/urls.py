from django.conf.urls import url, patterns
from app1.views import current_time, hours_ahead

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^time/$', current_time), # <--------It's a reference to an object, not a STRING !!!!!!
    url(r'^time/plus/(\d{1,2})/$', hours_ahead), # <---------- Parameters in URLS GO WITHIN PARENTHESIS!!!!!!
)