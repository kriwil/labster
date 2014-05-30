from django.conf.urls import patterns, include, url  # noqa


urlpatterns = patterns('labster.cms.views',  # nopep8
    url('^labs/$', 'lab_list'),
)
