INSTALL.md
==========

app environment setup.


-----

## getting started

this assumes development from a machine running osx >= *10.8*.

### prerequisites
* [homebrew >=*0.9.5*](http://mxcl.github.com/homebrew)
* [git >=*1.8.4.3*](http://git-scm.com)
* [git-extras >=*1.8.0*](http://github.com/visionmedia/git-extras)
* [hub >=*1.10.6*](http://github.com/defunkt/hub)
* [nvm](https://github.com/creationix/nvm)
* [nodejs >=*v0.10.26*](http://nodejs.org)
* [coffeescript >=*1.7.1*](http://coffeescript.org)
* [python *2.7.5*](http://python.org)

-----


## new environment setup


### install homebrew

[homebrew](http://mxcl.github.com/homebrew) simplifies the way packages are
installed and managed on osx. until a vagrant machine image is setup, osx
dependencies + packages will be installed using the `brew` command for
best consistency.

    $ ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"

make sure to add `brew` installed packages to the top of the executable path.
to do so append to your `~/.bash_profile`:

    $ echo "export PATH=/usr/local/bin:${PATH}" >> ~/.bash_profile


### OPTIONAL: install git + git-extras + hub

    $ brew update && brew install git git-extras hub


### install python
the app is be standardized to use *2.7.5* version. to install it:

    $ brew install python --framework --universal

**NOTE**: you might have to put python at your `$PATH` by editing `~/.bash_profile`

    $ echo "export PATH=/usr/local/share/python:${PATH}" >> ~/.bash_profile


### install node version manager, coffee-script
the app uses [node.js](http://nodejs.org) to build and bundle the front end.

    $ curl https://raw.github.com/creationix/nvm/master/install.sh | sh
    $ nvm install 0.10.26
    $ nvm use 0.10.26
    $ npm install -g coffee-script


-----


### install python dependencies

#### pip, virtualenv & virtualenvwrapper

the app uses [pip](http://pip-installer.org) to manage python dependencies.
[virtualenv](http://virtualenv.org) and [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org)
create isolated python environments so developers can work on more than one
python project without pip's packages overlapping.

install pip, virtualenv and virtualenvwrapper:

    $ sudo pip install virtualenv virtualenvwrapper


update your `.bash_profile` in your home directory to automatically invoke
the virtualenv scripts for shell windows. you can also reload this file by
invoking `. ~/.bash_profile` or simply exiting and re-opening your terminal.

your `~/.bash_profile` should have something like this:

    $ echo '# virtualenv + virtualenvwrapper for python' >> ~/.bash_profile
    $ echo "export WORKON_HOME=~/.virtualenvs" >> ~/.bash_profile
    $ echo ". /usr/local/bin/virtualenvwrapper.sh" >> ~/.bash_profile
    $ echo "export PIP_VIRTUALENV_BASE=$" >> ~/.bash_profile

the above script sets the `virtualenvwrapper` environments default directory
to the home directory in the folder `~/.virtualenvs`.
it then sources `virtualenvwrapper`.

*(make sure you have re-`source` your `.bash_profile` in your current terminal session.)*


##### setup the virtualenv project
use `virtualenvwrapper` to create a new virtualenv environment for the project.

    $ mkvirtualenv {{project-id}}

run: `workon` into your terminal prompt you should see all available environments.

_(make sure you see your project id: {{project-id}})_


-----


## project setup

we are now ready to setup the project from git to run & build locally


### setup the project from git

    $ workon {{project-id}}
    $ mkdir ~/work/{{project-id}} && cd ~/work/{{project-id}}
    $ git clone git@github.com:{{username}}/{{project-id}}.git
    $ cd {{project-id}}

    $ pip install -r requirements.txt
    $ paver bootstrap
    $ paver build


run `git hooks --install` inside the git project to change that project's
git hooks to use git-hooks hooks.


-----


now you're ready to head onto the [QUICKSTART.md](QUICKSTART.md) docs to
get up and running with a new project.
