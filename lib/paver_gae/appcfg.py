"""
  paver.ext.gae.appcfg
  ~~~~~~~~~~~~~~~~~~~~

  wrapper for working with the app engine sdk's `appcfg.py` command.


  :copyright: (c) 2014 by gregorynicholas.
  :license: MIT, see LICENSE for more details.
"""
from __future__ import unicode_literals
from paver.easy import options as opts
from paver.ext import utils


__all__ = ["appcfg"]


def appcfg(command, **flags):
  """
  wraps the app engine `appcfg.py` command with common parameters.

    :param command: string command to execute + run
  """
  for flag in opts.proj.appcfg.flags:
    flags.setdefault(flag, True)

  cap, err, quiet = utils.pop_sh_kwargs(flags)

  cwd = flags.pop("cwd", opts.proj.dirs.base)

  # a bit of trickery to support working with appcfg 'backends' commands
  backend_cwd = cwd
  backend_id = flags.pop("backend_id", "")
  if backend_id and backend_id != "":
    backend_cwd = ""

  flags.setdefault("skip_sdk_update_check", True)

  appcfg_sh = '{gae_sdk}/appcfg.py {command} . {backend_id} {flags} '
  oauth2 = True

  # setup password-based auth..
  if hasattr(opts.proj, 'password') and opts.proj.password is not "":
    appcfg_sh = _wrap_appcfg_sh(
      appcfg_sh, opts.proj.password)
    flags.pop('oauth2', None)  # remove the oauth2 flag when password exists
    oauth2 = False

  flags = utils.to_flags(flags)

  ctx = dict(
    command=command,
    flags=flags,
    backend_id=backend_id,
    gae_sdk=opts.gae.sdk.root,
    error=err,
    capture=cap,
    quiet=quiet)

  if cap:
    res = utils.sh(appcfg_sh, cwd=cwd, _cwd=backend_cwd, **ctx)

    # check for existing oauth2 cookie file..
    if oauth2 and 'application does not exist' in res.lower():
      raise Exception(
        "oauth failed. make sure: `~/.appcfg_oauth2_tokens` doesn't exist.")
    else:
      print res

    return res
  else:
    return utils.sh(appcfg_sh, cwd=cwd, _cwd=backend_cwd, **ctx)


def _wrap_appcfg_sh(appcfg_sh, password):
  """
  wraps an `appcfg` command string to accept the password arg.
  """
  return 'echo "{password}" | {appcfg_sh} --passin '.format(
    password=password,
    appcfg_sh=appcfg_sh)
