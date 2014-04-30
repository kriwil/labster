from django.conf.urls import patterns, include, url


urlpatterns = patterns('labster',  # nopep8

    # all API urls should be under api/v1 path
    url('^api/v1/', include('labster.api_urls')),
)
