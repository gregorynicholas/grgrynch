application configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

see: https://developers.google.com/appengine/docs/python/config/appconfig



force python precompilation on deploy:

    derived_file_type:
    - python_precompiled



by default, files declared in static file handlers are uploaded as static data
and are only served to end users, they cannot be read by an application.
if this field is set to true, the files are also uploaded as code data so your
application can read them. Both uploads are charged against your code and
static data storage resource quotas

    application_readable



skip_files has the following default:

    skip_files:
    - ^(.*/)?#.*#
    - ^(.*/)?.*~
    - ^(.*/)?.*\.py[co]
    - ^(.*/)?.*/RCS/.*
    - ^(.*/)?\..*

    # skip files whose names end in .bak:
    - ^(.*/)?\.bak


### libraries

see: https://developers.google.com/appengine/docs/python/tools/libraries27
