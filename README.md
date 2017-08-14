GRGRYNCH
========

source code for [GREGORYNICHOLAS.com](http://gregorynicholas.com).

[![circleci](https://circleci.com/gh/gregorynicholas/grgrynch.svg?style=svg)](https://circleci.com/gh/gregorynicholas/grgrynch)


-----
<br>
<br>


* i:   [docs / INSTALL](docs/INSTALL.md)
* ii:  [docs / QUICKSTART](docs/QUICKSTART.md)
* iii: [docs / CLIENT](docs/CLIENT.md)
* iv:  [docs / BUMP](docs/BUMP.md)


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



-----
<br>
<br>



#### BOOTSTRAP PROJECT:

```sh
#pyenv exec paver bootstrap;
pyenv exec paver bootstrap_server;
pyenv rehash;
pyenv exec paver bootstrap_server_gae_sdk;
pyenv rehash;
pyenv exec paver install_sdk;  #< gae.sdk.install_sdk
pyenv rehash;

alias paver='pyenv exec paver ';
paver bootstrap_client;
paver gae:datastore_init;
```


#### BUILD, RUN COMMANDS:

```sh
pyenv activate GRGRYNCH-2.7.11;
paver build;
paver build_server;
paver build_client;
paver gae:server_run;
paver gae:server_tail;
paver gae:server_stop;

```

>one-liner:

```sh
bin/build-run; bin/tail;
```


#### SUPERVISOR CTL COMMANDS:

```sh
_kill() {
  ps aux |  grep "$1" |  grep -v "grep" |  awk '{print $2}' |  xargs kill -9;
};

paver build;
paver gae:server_stop;

_kill  "dev_appserver.py";
_kill  "_python_runtime.py";

paver gae:server_run;
supervisorctl start devappserver-local;
supervisorctl restart devappserver-local;
supervisorctl stop devappserver-local;
```



#### RELEASE, DEPLOY COMMANDS:

```sh

#@ RELEASE + DEPLOY
#@
paver dist_build --env_id qa;
paver dist_build --env_id prod;
cd .dist/;
appcfg.py update --no_usage_reporting --skip_sdk_update_check --verbose .;
cd -;
```

>-or-

```sh
bin/dist
```

>-or-

```sh
pyenv exec paver gae:deploy;
```



-----
<br>
<br>



* i:   [docs / quickstart](docs/QUICKSTART.md)
* ii:  [docs / environment bootstrapping](docs/INSTALL.md)
* iii: [docs / client](docs/CLIENT.md)
* iv:  [docs / versioning](docs/BUMP.md)
