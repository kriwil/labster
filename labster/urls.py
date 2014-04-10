from django.conf.urls import patterns, url


urlpatterns = patterns('',  # nopep8
    url('^api/labs/', 'labster.api.views.questions'),
    url('^labs/add/', 'labster.labs.views.add_lab'),
    url('^labs/lists/', 'labster.labs.views.lists'),
)
