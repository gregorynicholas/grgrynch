cron job service api configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

see: https://developers.google.com/appengine/docs/python/config/cron


NOTE: to target a backend, we specify the name defined in backends.yaml.


### definitions

example definition:

    schedule: every 1 12 hours
    schedule: every day 03:00
    target: backend-v0-0-0


schedule formats:

    every 12 hours
    every 5 minutes from 10:00 to 14:00
    2nd,third mon,wed,thu of march 17:00
    every monday 09:00
    1st monday of sep,oct,nov 17:00
    every day 00:00


regular interval schedule form:

    every N (hours|mins|minutes) ["from" (time) "to" (time)]

* N specifies a number
* hours or minutes (you can also use mins) specifies the unit of time
* time specifies a time of day, as HH:MM in 24 hour time

