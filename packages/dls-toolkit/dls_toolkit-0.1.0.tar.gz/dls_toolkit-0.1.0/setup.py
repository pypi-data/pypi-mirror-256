# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dls_toolkit', 'dls_toolkit.gdrive']

package_data = \
{'': ['*']}

install_requires = \
['google-api-python-client>=2.117.0,<3.0.0']

setup_kwargs = {
    'name': 'dls-toolkit',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Dustin Sampson',
    'author_email': 'dustin@sparkgeo.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
