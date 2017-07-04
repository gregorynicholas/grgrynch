CLIENT.md
=========

app client built with gruntjs + angularjs + coffee-script + stylus.


-----

### getting started

this assumes development from a machine running *`osx@>=10.7`*.

### prerequisites
* homebrew      >=*0.9.5*    ([http://mxcl.github.com/homebrew](http://mxcl.github.com/homebrew))
* nodejs        >=*v0.10.7*  ([http://nodejs.org](http://nodejs.org))
* npm           >=*1.2.21*   ([http://npmjs.org](http://npmjs.org))
* stylus        >=*0.31.0*   ([http://learnboost.github.io/stylus/](http://learnboost.github.io/stylus/))
* coffeescript  >=*1.7.1*    ([http://coffeescript.org](http://coffeescript.org))
* grunt         >=*0.4.1*    ([http://gruntjs.com](http://gruntjs.com))
* grunt-cli     >=*0.1.8*    ([http://gruntjs.com](http://gruntjs.com))
* bower         >=*1.8.0*    ([http://todo](http://todo))

<br />

-----

### environment setup

before continuing, please make sure you have gone through the [INSTALL.md](../docs/INSTALL.md)
for a consistent environment setup.


### install grunt + coffee-script + bower + stylus

    $ npm install -g coffee-script
    $ npm install -g grunt@0.4.1
    $ npm install -g bower@1.8.0
    $ npm install -g stylus@0.31.0


### install grunt-cli

this puts the `grunt` command in your system path, allowing it to be run from
any directory (don't ask me why this is separate..):

    $ npm install -g grunt-cli@0.1.8


### install project + dependencies

    $ cd ./client
    $ npm install
    $ bower install
