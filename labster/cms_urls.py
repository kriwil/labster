from django.conf.urls import patterns, include, url  # noqa


urlpatterns = patterns('labster.cms.views',  # nopep8
    url('^labs/$', 'lab_list'),
    url('^labs/(?P<id>\d+)/$', 'lab_detail'),
    url('^labs/(?P<lab_id>\d+)/create-quiz-block/$', 'create_quiz_block', name='labster_create_quiz_block'),

    url('^lab-proxies/(?P<id>\d+)/$', 'lab_proxy_detail'),

    url('^quiz-blocks/(?P<id>\d+)/$', 'quiz_block_detail', name='labster_quiz_block_detail'),
    url('^quiz-blocks/(?P<quiz_block_id>\d+)/create-problem/$', 'create_problem', name='labster_create_problem'),
)
