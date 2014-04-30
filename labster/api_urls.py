from django.conf.urls import patterns, url


urlpatterns = patterns('labster',  # nopep8

    url('^labs/(?P<lab_proxy_id>\d+)/$', 'lab_proxies.views.lab_proxy_detail'),
    url('^labs/(?P<lab_proxy_id>\d+)/save/$', 'game_user_save.views.save_detail'),

    ## deprecated
    # Game Error Info
    url('^game_error_info/post/$', 'game_error_info.views.game_error_post'),

    # User Device Info
    url('^user_device_info/post/$', 'user_device_info.views.user_device_post'),
)
