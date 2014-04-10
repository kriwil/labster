from django.conf.urls import patterns, url


urlpatterns = patterns('',  # nopep8
    url('^api/labs/', 'labster.api.views.questions'),
    # Labs
    url('^labs/add/', 'labster.labs.views.add_lab'),
    url(r'^labs/', 'labster.labs.views.index'),
    # Language Lab
    url('^language_labs/add/', 'labster.language_labs.views.add_language_lab'),
    url('^language_labs/', 'labster.language_labs.views.index'),
)
