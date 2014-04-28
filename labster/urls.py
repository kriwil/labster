from django.conf.urls import patterns, url


urlpatterns = patterns('',  # nopep8
    url('^api/labs/(?P<proxy_id>\d+)/$', 'labster.api.views.quizblocks'),

    # Labs
    # url(r'^labs/$', 'labster.labs.views.index'),
    # url(r'^labs/add/$', 'labster.labs.views.add'),
    # url(r'^labs/(?P<lab_id>\d+)/update/$', 'labster.labs.views.update'),
    # url(r'^labs/(?P<lab_id>\d+)/delete/$', 'labster.labs.views.delete'),

    # Language Lab
    # url(r'^language_labs/$', 'labster.language_labs.views.index'),
    # url(r'^language_labs/add/$', 'labster.language_labs.views.add'),
    # url(r'^language_labs/(?P<lang_id>\d+)/update/$', 'labster.language_labs.views.update'),
    # url(r'^language_labs/(?P<lang_id>\d+)/delete/$', 'labster.language_labs.views.delete'),

    # Game Error Info
    url('^game_error_info/post/$', 'labster.game_error_info.views.game_error_post'),

    # User Device Info
    url('^user_device_info/post/$', 'labster.user_device_info.views.user_device_post'),

    # Game User Save File
    url('^game_user_save/$', 'labster.game_user_save.views.game_user_save_block'),
)
