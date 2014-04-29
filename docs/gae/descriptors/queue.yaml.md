taskqueue service api configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

see: https://developers.google.com/appengine/docs/python/config/queue


NOTE: tasks will stop retrying ONLY when both "task_retry_limit" and
"task_age_limit" limits are reached.


