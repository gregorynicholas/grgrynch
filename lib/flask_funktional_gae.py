"""
  flask.ext.funktional_gae
  ~~~~~~~~~~~~~~~~~~~~~~~~

  flask extension to make functional testing of flask applications with the
  app engine sdk easier


  :copyright: (c) 2015 by gregorynicholas.

"""
from __future__ import unicode_literals
from flask.ext.funktional import TestCase as FunkTestCase
from google.appengine.ext import testbed
from google.appengine.api import queueinfo


__all__ = ["TestCase", "init_testbed", "testbed"]


_queue_descriptor = """
queue:
- name: default
  rate: 10/s

- name: crazy-queue
  rate: 2000/d
  bucket_size: 10
"""


# api stubs that require a little more work to setup..

def init_taskqueue_stub(tb):
  tb.init_taskqueue_stub()
  tq_stub = tb.get_stub(testbed.TASKQUEUE_SERVICE_NAME)
  tq_stub.queue_yaml_parser = (
    lambda x: queueinfo.LoadSingleQueue(_queue_descriptor))


def init_images_stub(tb):
  try:
    import PIL
  except (ImportError, testbed.StubNotSupportedError):
    pass  # die silently for now..
  else:
    tb.init_images_stub()


def init_search_stub(tb):
  from google.appengine.api.search.simple_search_stub import SearchServiceStub
  tb._register_stub("search", SearchServiceStub())


_service_tb_map = {
  "app_identity_service": testbed.Testbed.init_app_identity_stub,
  "blobstore": testbed.Testbed.init_blobstore_stub,
  "capability_service": testbed.Testbed.init_capability_stub,
  "channel": testbed.Testbed.init_channel_stub,
  "datastore_v3": testbed.Testbed.init_datastore_v3_stub,
  "file": testbed.Testbed.init_files_stub,
  "logservice": testbed.Testbed.init_logservice_stub,
  "memcache": testbed.Testbed.init_memcache_stub,
  "mail": testbed.Testbed.init_mail_stub,
  "urlfetch": testbed.Testbed.init_urlfetch_stub,
  "user": testbed.Testbed.init_user_stub,
  "xmpp": testbed.Testbed.init_xmpp_stub,
  "search": init_search_stub,
  testbed.IMAGES_SERVICE_NAME: init_images_stub,
  testbed.TASKQUEUE_SERVICE_NAME: init_taskqueue_stub,
}


def init_testbed(services=None):
  """
  tries to enable all api services by default.  also adds default taskqueue
  configurations.

  factores that the cost of time spent monkey'ing with this shit and writing
  all of this boilerplate code is obviously not worth the 0.020ms it takes to
  execute this setup. if you make this this far into the code, write your own,
  more performant method if needed.

    :param services: instance of a string list for app engine api services
    :returns: instance of a `testbed.Testbed()` object
  """
  services = services or testbed.INIT_STUB_METHOD_NAMES.keys()
  rv = testbed.Testbed()
  rv.activate()
  [_service_tb_map[s].__call__(rv) for s in services if s in _service_tb_map]
  return rv


class TestCase(FunkTestCase):
  """
  enable app engine sdk stubs and disable services.  this will replace calls
  to the service with calls to the service stub.
  """
  tb = None

  def setup_pre_hook(self):
    """
    """
    self.tb = init_testbed()

  def teardown_post_hook(self):
    """
    deactivate the testbed once the tests are completed.
    """
    if hasattr(self, "tb") and self.tb:
      self.tb.deactivate()

  # mail api helpers..
  # ---------------------------------------------------------------------------

  @property
  def mail_stub(self):
    return self.tb.get_stub(testbed.MAIL_SERVICE_NAME)

  def get_sent_messages(
    self, to=None, sender=None, subject=None, body=None, html=None):
    """
    Get a list of ``mail.EmailMessage`` objects sent via the Mail API.
    """
    return self.mail_stub.get_sent_messages(
      to=to, sender=sender, subject=subject, body=body, html=html)

  def assertMailSent(
    self, to=None, sender=None, subject=None, body=None, html=None):
    messages = self.get_sent_messages(
      to=to, sender=sender, subject=subject, body=body, html=html)
    self.assertNotEqual(
      0, len(messages),
      "No matching email messages were sent.")

  # memcache api helpers..
  # ---------------------------------------------------------------------------

  @property
  def memcache_stub(self):
    return self.tb.get_stub(testbed.MEMCACHE_SERVICE_NAME)

  def assertMemcacheHits(self, hits):
    """Asserts that the memcache API has had `hits` successful lookups."""
    self.assertEqual(
      hits, self.memcache_stub.get_stats()['hits'])

  def assertMemcacheItems(self, items):
    """Asserts that the memcache API has `items` key-value pairs."""
    self.assertEqual(
      items, self.memcache_stub.get_stats()['items'])

  # taskqueue api helpers..
  # ---------------------------------------------------------------------------

  @property
  def taskqueue_stub(self):
    return self.tb.get_stub(testbed.TASKQUEUE_SERVICE_NAME)

  def get_tasks(self, url=None, name=None, queue_names=None):
    """
    Returns a list of `Task`_ objects with the specified criteria.

      :param url:
          URL criteria tasks must match. If `url` is `None`, all tasks
          will be matched.
      :param name:
          name criteria tasks must match. If `name` is `None`, all tasks
          will be matched.
      :param queue_names:
          queue name criteria tasks must match. If `queue_name` is `None`
          tasks in all queues will be matched."""
    return self.taskqueue_stub.get_filtered_tasks(
      url=url,
      name=name,
      queue_names=queue_names)

  def assertTasksInQueue(self, n=None, url=None, name=None, queue_names=None):
    """
    search for `task`_ objects matching the given criteria and assert that
    there are `n` tasks.

      :usage::

        deferred.defer(some_task, _name='some_task')
        self.assertTasksInQueue(n=1, name='some_task')

      :param n:
          the number of tasks in the queue. If not specified, `n` defaults
          to 0.
      :param url:
          URL criteria tasks must match. If `url` is `None`, all tasks
          will be matched.
      :param name:
          name criteria tasks must match. If `name` is `None`, all tasks
          will be matched.
      :param queue_names:
          queue name criteria tasks must match. If `queue_name` is `None`
          tasks in all queues will be matched."""
    tasks = self.get_tasks(
      url=url,
      name=name,
      queue_names=queue_names)
    self.assertEqual(n or 0, len(tasks))

  # blobstore api helpers..
  # ---------------------------------------------------------------------------

  @property
  def blobstore_stub(self):
    return self.tb.get_stub(testbed.BLOBSTORE_SERVICE_NAME)

  def create_blob(self, blob_key, data):
    """
    create new blob and put in storage and datastore.

      :param blob_key: String blob-key of new blob.
      :param data: data of new blob.

      :returns:
        new datastore blobinfo entity without blob meta-data fields.
    """
    return self.blobstore_stub.CreateBlob(blob_key, data)
