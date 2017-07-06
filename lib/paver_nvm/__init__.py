# encoding: utf-8
"""
  paver.ext.nvm
  ~~~~~~~~~~~~~


  :copyright: (c) 2014 by gregorynicholas.

"""
from __future__ import unicode_literals
from paver.ext.http import curl
from paver.ext.utils import sh


__all__ = [
  'install',
]


def get_latest_install_url():
  """
  """
  _fmt = '%{url_effective}'
  _url = 'http://latest.nvm.sh'
  _url = curl('--disable --silent --write-out "{_fmt}" --location --show-error {_url} --output /dev/null', _fmt=_fmt, _url=_url)
  _url = _url.strip()
  _url = _url.replace('https://github.com/creationix/nvm/releases/tag', 'https://raw.githubusercontent.com/creationix/nvm')
  return _url + '/install.sh'
  

def install():
  _url = get_latest_install_url()
  _sh = curl("--disable --silent --show-error -o- {_url}", _url=_url)

  _install = sh(_sh, error=True, capture=True)

  if 'nvm is already installed in' in _install:
  	print('nvm is already installed..')
  	return True

  else:
  	return _install
