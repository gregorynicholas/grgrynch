grgrynch
========

source code for [gregorynicholas.com](http://gregorynicholas.com) (a google
appengine app).

<br />

-----

* [INSTALL.md](docs/INSTALL.md)
* [QUICKSTART.md](docs/QUICKSTART.md)

-----

<br />

quick'n'dirty shell install script:


    $ mkvirtualenv --no-site-packages grgrynch
    $ pip install -r requirements.txt
    $ paver bootstrap
    $ paver gae:install_sdk
    $ paver bootstrap_init_dirs
    $ paver gae:datastore_init
    $ paver gae:server_run
    $ paver gae:server_tail
    $ paver gae:server_stop
