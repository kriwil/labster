from django.conf.urls import patterns, url


urlpatterns = patterns('',  # nopep8
    url('^labs/$', 'labs_detail'),
)
