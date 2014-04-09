from django.conf.urls import patterns, url


urlpatterns = patterns('',  # nopep8
    url('^api/labs/', 'labster.api.views.questions'),
)
