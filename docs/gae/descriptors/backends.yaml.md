backends service api configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

see: https://developers.google.com/appengine/docs/python/config/backends


### definition

* instances
    * an integer between 1 and 20 indicating the number of instances to assign to the given backend
    * defaults to 1 if unspecified
    * the instance number is also referred to as the INSTANCE_ID

* class
    class memory    limit     cpu limit    cost per hour*
    B1              128MB     600MHz       $0.08
    B2(default)     256MB     1.2GHz       $0.16
    B4              512MB     2.4GHz       $0.32
    B8              1024MB    4.8GHz       $0.64

* start
  * specifies a script to run at start time
  * adding directive is equivalent to defining a handler for `/_ah/start`, but only applies to a single backend
  * the value should be a filename relative to the application's root directory

* options
    * a list of boolean settings, which can include one or more of the following options:

    dynamic:     choice of "resident" or "dynamic"
    failfast:    disables pending queue
    public:      enables public http based access
