===================
Labster app for edX
===================

- git clone https://github.com/kriwil/labster.git
- (include labster in vagrant mount)
- vagrant ssh
- sudo su edxapp
- pip install -e /path/to/labster/

tests
-----

::

  # create virtualenv (run once)
  virtualenv env
  source env/bin/activate

  # install requiements (run once)
  pip install -r requirements.txt

  # run the tests
  python manage.py test labster
