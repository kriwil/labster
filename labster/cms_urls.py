from django.conf.urls import patterns, include, url  # noqa


urlpatterns = patterns('labster.cms.views',  # nopep8
    url('^labs/$', 'lab_list'),
    url('^labs/(?P<id>\d+)/$', 'lab_detail'),
    url('^quiz-blocks/(?P<id>\d+)/$', 'quiz_block_detail'),
)
