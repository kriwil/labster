from django.conf.urls import patterns, include, url


urlpatterns = patterns('labster',  # nopep8

    # all API urls should be under api/v1 path
    url('^api/v1/', include('labster.api_v1_urls', namespace='labster_api_v1')),
    url('^api/v2/', include('labster.api_v2_urls', namespace='labster-api-v2')),
)
