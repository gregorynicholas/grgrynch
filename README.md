GRGRYNCH
========

source code for [GREGORYNICHOLAS.com](http://gregorynicholas.com).

[![circleci](https://circleci.com/gh/gregorynicholas/grgrynch.svg?style=svg)](https://circleci.com/gh/gregorynicholas/grgrynch)


-----
<br>
<br>


* i: [INSTALL.md](docs/INSTALL.md)
* ii: [QUICKSTART.md](docs/QUICKSTART.md)
* iii: [CLIENT.md](docs/CLIENT.md)


-----
<br>
<br>


### LOCAL ENVIRONMENT SETUP:


#### PYENV INSTALL, SETUP:

```sh
export PYENV_ROOT="$HOME/.pyenv";
export PATH="$PYENV_ROOT/bin:$PATH";
export PYENV_VIRTUALENV_VERBOSE_ACTIVATE=1;

[[ ! -d "$PYENV_ROOT" ]] && git clone https://github.com/pyenv/pyenv.git "$PYENV_ROOT";
[[ ! -d "$(pyenv root)/plugins/pyenv-virtualenv" ]] && git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv;
[[ ! -d "$(pyenv root)/plugins/pyenv-pip-rehash" ]] && git clone https://github.com/yyuu/pyenv-pip-rehash.git $(pyenv root)/plugins/pyenv-pip-rehash;

pyenv rehash;
eval "$(pyenv init -)" && eval "$(pyenv virtualenv-init -)";

```

#### PYENV-VIRTUALENV SETUP, CONFIG:

```sh
pyenv virtualenv 2.7.11 GRGRYNCH-2.7.11;
pyenv activate GRGRYNCH-2.7.11;
pyenv exec pip install --disable-pip-version-check --verbose --upgrade pip;

# <TODO> how to point to --config ./build/pip.conf

pyenv exec pip install --disable-pip-version-check --verbose -r ./build/requirements/1.0_paver-deps.txt && pyenv rehash;
pyenv exec pip install --disable-pip-version-check --verbose -r ./build/requirements/2.0_paver.txt && pyenv rehash;
```


<TODO>
    @see https://github.com/GoogleCloudPlatform/continuous-deployment-circle/blob/master/circle.yml


#### bootstrap project:

```sh
#pyenv exec paver bootstrap;
pyenv exec paver bootstrap_server;
pyenv rehash;
pyenv exec paver bootstrap_server_gae_sdk;
pyenv rehash;
pyenv exec paver install_sdk;  #< gae.sdk.install_sdk
pyenv exec paver bootstrap_client;
pyenv exec paver gae:datastore_init;
```


#### run shell commands:

```sh
pyenv activate GRGRYNCH-2.7.11;
pyenv exec paver build;
pyenv exec paver build_client;
pyenv exec paver gae:server_run;
pyenv exec paver gae:server_tail;
pyenv exec paver gae:server_stop;
```


-----
<br>
<br>


```sh
$ appcfg.py -A grgrynch-dev-01 -v v0-0-1 download_app ../deployed;
```
