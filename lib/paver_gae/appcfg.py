"""
  paver.ext.gae.appcfg
  ~~~~~~~~~~~~~~~~~~~~

  wrapper for working with the app-engine sdk's `appcfg.py` cli.


  :copyright: (c) 2014 by gregorynicholas.

"""
from __future__ import unicode_literals
from paver.easy import options as opts
from paver.ext import utils
from paver.ext.utils import sh


__all__ = [
  "appcfg",
]


def appcfg(command, **flags):
  """
  wraps the app-engine sdk `appcfg.py` command with common parameters.

    :param command: string command to execute + run
    :param flags: dict of key/value options passed along to `appcfg.py`
  """
  #: set defaults..
  flags.setdefault("skip_sdk_update_check", True)
  for flag in opts.proj.appcfg.flags:
    flags.setdefault(flag, True)

  capt, err, quiet = utils.pop_sh_kwargs(flags)
  cwd = flags.pop("cwd", opts.proj.dirs.base)

  #: a bit of trickery to support working with appcfg 'backends' sub-commands
  backend_cwd = cwd
  backend_id = flags.pop("backend_id", "")
  if backend_id and backend_id != "":
    backend_cwd = ""

  appcfg_sh = '{gae_sdk}/appcfg.py {command} . {backend_id} {flags}'
  oauth2 = True

  #: handle password-based auth..
  if hasattr(opts.proj, 'password') and opts.proj.password is not "":
    appcfg_sh = _wrap_appcfg_sh(
      appcfg_sh, opts.proj.email, opts.proj.password)

    # remove the oauth2 flag when password exists
    flags.pop('oauth2', None)
    flags.pop('noauth_local_webserver', None)
    oauth2 = False

  flags = utils.to_flags(flags)

  ctx = dict(
    command=command,
    flags=flags,
    backend_id=backend_id,
    gae_sdk=opts.gae.sdk.root,
    error=err,
    capture=capt,
    quiet=quiet)

  if capt:
    appcfg_sh = appcfg_sh.format(**ctx)
    # print 'running:', appcfg_sh

    res = utils.sh(appcfg_sh, cwd=cwd, _cwd=backend_cwd)

    #: check for existing oauth2 cookie file..
    if res and (oauth2 and 'application does not exist' in res.lower()):
      raise Exception(
        "oauth failed. make sure: `~/.appcfg_oauth2_tokens` doesn't exist.")
    else:
      print res

    return res

  else:
    return utils.sh(appcfg_sh, cwd=cwd, _cwd=backend_cwd, **ctx)


def _wrap_appcfg_sh(appcfg_sh, email, password):
  """
  wraps an `appcfg` command string to accept the password arg.
  """
  return 'echo "{password}" | {appcfg_sh} --email {email} --passin '.format(
    email=email,
    password=password,
    appcfg_sh=appcfg_sh)
