from django.conf.urls import patterns, url


urlpatterns = patterns('labster',  # nopep8

    url('^labs/(?P<lab_proxy_id>\d+)/$', 'lab_proxies.views.lab_proxy_detail'),
    url('^labs/(?P<lab_proxy_id>\d+)/save/$', 'game_user_save.views.save_detail'),
    url('^labs/(?P<lab_proxy_id>\d+)/log-error/$', 'game_error_info.views.log_error'),
    url('^labs/(?P<lab_proxy_id>\d+)/log-device/$', 'user_device_info.views.log_device'),
)
