QUICKSTART.md
=============

app quickstart.


-----

## new project quickstart

-----


#### virtualenv setup

    $ mkvirtualenv {{project-id}}
    $ cd ~/.virtualenvs/{{project-id}}


#### appengine setup

    $ curl -O http://googleappengine.googlecode.com/files/google_appengine_1.8.9.zip
    $ unzip -d ./ -oq google_appengine_1.8.9.zip && rm google_appengine_1.8.9.zip
    $ export PATH="~/.virtualenvs/{{project-id}}/google_appengine:${PATH}"


#### appengine x virtualenv fix

    $ echo "$HOME/.virtualenvs/{{project-id}}/google_appengine" >> lib/python2.7/site-packages/gae.pth
    $ echo "import dev_appserver; dev_appserver.fix_sys_path()" >> lib/python2.7/site-packages/gae.pth


-----


####  application setup

    $ pip install -r requirements.txt


copy project over, update project code. update environ specific configs, build
configs:

    - .env
    - release.sh
    - rebuild.sh
    - circle.yml
    - build/project.yaml
    - app/config/__init__.py
    - client/app/styles/app.styl
    - client/app/index.html
    - client/app/views/index.html
    - client/app/views/header.html
    - client/README.md

    $ paver bootstrap
