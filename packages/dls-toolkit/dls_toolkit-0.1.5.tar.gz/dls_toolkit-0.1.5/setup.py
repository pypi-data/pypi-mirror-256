# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dls_toolkit', 'dls_toolkit.gdrive']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.34.39,<2.0.0',
 'google-api-python-client>=2.117.0,<3.0.0',
 'python-dateutil>=2.8.2,<3.0.0']

setup_kwargs = {
    'name': 'dls-toolkit',
    'version': '0.1.5',
    'description': 'A set of my common tools.',
    'long_description': '# DLS Toolkit\n\n[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)\n\n## Description\n\nA set of my common tools.\n\n\n## Installation\n\n`pip install dls-toolkit`\n\n## Environment Variables\n\n```\n\n# Google Cloud\n\nGOOGLE_APPLICATION_CREDENTIALS - Path to the Google Cloud Service Account JSON file.\n    Needs access to:\n        - Google Drive\n\n# AWS\n\nAWS_ACCESS_KEY_ID - AWS Access Key\nAWS_SECRET_ACCESS_KEY - AWS Secret Access Key\nAWS_REGION - AWS Region\n    Needs access to:\n        - Billing\n\n```\n\n## License\n\nThis project is licensed under the [MIT License](LICENSE).\n\n## Contact\n\n- [GitHub](https://github.com/your-username)\n',
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
