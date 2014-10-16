from django.conf.urls import patterns, include, url


urlpatterns = patterns('labster',  # nopep8
    url('^api/', include('labster.api_urls', namespace='labster-api')),
    url('^demo-lab/$', 'lms.views.demo_lab', name='labster_demo_lab'),
)
