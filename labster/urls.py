from django.conf.urls import patterns, url


urlpatterns = patterns('labster',  # nopep8

    # all API urls should be under api/v1 path
    url('^api/v1/labs/(?P<lab_proxy_id>\d+)/$', 'lab_proxies.views.lab_proxy_detail'),

    # Game Error Info
    url('^game_error_info/post/$', 'game_error_info.views.game_error_post'),

    # User Device Info
    url('^user_device_info/post/$', 'user_device_info.views.user_device_post'),

    # Game User Save File
    url('^game_user_save/$', 'game_user_save.views.game_user_save_block'),
)
