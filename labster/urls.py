from django.conf.urls import patterns, url


urlpatterns = patterns('',  # nopep8
    url('^api/labs/', 'labster.api.views.questions'),
    # Labs
    url(r'^labs/$', 'labster.labs.views.index'),
    url(r'^labs/add/$', 'labster.labs.views.add'),
    url(r'^labs/(?P<lab_id>\d+)/update/$', 'labster.labs.views.update'),
    url(r'^labs/(?P<lab_id>\d+)/delete/$', 'labster.labs.views.delete'),
    # Language Lab
    url(r'^language_labs/$', 'labster.language_labs.views.index'),
    url(r'^language_labs/add/$', 'labster.language_labs.views.add'),
    url(r'^language_labs/(?P<lang_id>\d+)/update/$', 'labster.language_labs.views.update'),
    url(r'^language_labs/(?P<lang_id>\d+)/delete/$', 'labster.language_labs.views.delete'),
)
