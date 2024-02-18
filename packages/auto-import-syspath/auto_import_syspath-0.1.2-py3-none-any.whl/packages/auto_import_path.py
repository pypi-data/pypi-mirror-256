import os
import sys

from os.path import join, abspath, basename


def __found_before_path__(path_name: str, relative_path: str = None):
	__before_path__ = None
	__path__ = relative_path if relative_path else os.getcwd()

	while True:
		if basename(str(__path__).lower()) == path_name.lower():
			return __path__

		if __path__ in os.getcwd().split('\\')[0] + "\\":
			raise Exception("Modulo não encontrado")

		__before_path__ = abspath(join(__path__, '..'))

		print(__path__)
		__path__ = __before_path__


def import_sys_path(path_name: str, relative_path: str = None):
	path = __found_before_path__(path_name, relative_path)
	sys.path.append(path)


def import_python_module(module):
    return globals().get(module) == __import__(module)
    
import_sys_path('auto_import_path')
    
# import_python_module('setup')

import setup

setup.VERSION
