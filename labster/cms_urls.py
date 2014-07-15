from django.conf.urls import patterns, include, url  # noqa


urlpatterns = patterns('labster.cms.views',  # nopep8
    url('^duplicate-lab/$', 'duplicate_lab', name='labster_duplicate_lab'),
)
