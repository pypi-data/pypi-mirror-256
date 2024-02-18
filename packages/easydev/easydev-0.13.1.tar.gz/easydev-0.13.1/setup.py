# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['easydev', 'easydev.share', 'share']

package_data = \
{'': ['*'],
 'easydev.share': ['themes/cno/*',
                   'themes/cno/static/*',
                   'themes/standard/*',
                   'themes/standard/static/*'],
 'share': ['themes/cno/*',
           'themes/cno/static/*',
           'themes/standard/*',
           'themes/standard/static/*']}

install_requires = \
['colorama>=0.4.6,<0.5.0',
 'colorlog>=6.8.2,<7.0.0',
 'line-profiler>=4.1.2,<5.0.0',
 'pexpect>=4.9.0,<5.0.0',
 'platformdirs>=4.2.0,<5.0.0']

setup_kwargs = {
    'name': 'easydev',
    'version': '0.13.1',
    'description': 'Commn utilities to ease development of Python packages',
    'long_description': "easydev\n##########\n\n.. image:: https://badge.fury.io/py/easydev.svg\n    :target: https://pypi.python.org/pypi/easydev\n\n.. image:: https://github.com/cokelaer/easydev/actions/workflows/main.yml/badge.svg\n    :target: https://github.com/cokelaer/easydev/actions/workflows/main.yml\n\n\n.. image:: https://coveralls.io/repos/cokelaer/easydev/badge.svg?branch=main\n   :target: https://coveralls.io/r/cokelaer/easydev?branch=main\n\n\n\n\n:documentation: http://easydev-python.readthedocs.io/en/latest/\n:contributions: Please join https://github.com/cokelaer/easydev\n:source: Please use https://github.com/cokelaer/easydev\n:issues: Please use https://github.com/cokelaer/easydev/issues\n:Python version supported: 3.7, 3.8, 3.9, 3.10\n\n\nThe  `easydev <http://pypi.python.org/pypi/easydev/>`_ package\nprovides miscellaneous functions that are repeatidly used during\nthe development of Python packages. The goal is to help developers on\nspeeding up their own dev. It has been used also as an incubator for other\npackages (e.g., http://pypi.python.org/pypi/colormap) and is stable.\n\n.. warning:: I'm not pretending to provide universal and bug-free tools. The\n    tools provided may also change. However, **easydev** is used\n    in a few other packages such as\n    `bioservices <https://pypi.python.org/pypi/bioservices>`_,\n    `sequana <https://sequana.readthedocs.io>`_ or\n    `GDSCTools <https://sequana.readthedocs.io>`_ to give a few\n    examples.\n\nChangelog\n~~~~~~~~~\n\n========= ==========================================================================\nVersion   Description\n========= ==========================================================================\n0.13.1    * fix get_dependencies\n0.13.0    * fix requirements (line_profiler) and CI\n0.12.2    * For developers: move to pyprojet. add precomit\n          * replace pkg_resources (deprecated) with importlib\n          * replace appdirs with more generic platformdirs\n========= ==========================================================================\n",
    'author': 'Thomas Cokelaer',
    'author_email': 'thomas.cokelaer@pasteur.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
