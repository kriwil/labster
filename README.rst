===================
Labster app for edX
===================

- git clone https://github.com/kriwil/labster.git
- (include labster in vagrant mount)
- vagrant ssh
- sudo su edxapp
- pip install -e /path/to/labster/

edX
---

::
  # lms/envs/common.py
  FEATURES = {
    ...
    'LABSTER': True,
  }
  
  if FAETURES.get('LABSTER'):
    INSTALLED_APS += ('labster',)
    
  
  # lms/urls.py
  if settings.FEATURES.get('LABSTER'):
    urlpatterns += (
      url('^labster/', include('labster.urls')),
    )
