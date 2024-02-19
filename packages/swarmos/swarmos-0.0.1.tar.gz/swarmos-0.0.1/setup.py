# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['swarmos']

package_data = \
{'': ['*']}

install_requires = \
['swarms', 'zetascale']

setup_kwargs = {
    'name': 'swarmos',
    'version': '0.0.1',
    'description': 'Paper - Pytorch',
    'long_description': "[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# SwarmOS\nAn all-new OS that orchestrates autonomous agents as workers to execute tasks. Inspired by Andrej Karpathy's vision but scaling them up to the thousands of agent OS to create a virtual cloud of agent OSs. We'll be using the Swarms to create the app for it's radical simplicity, bleeding-edge performance, and consistent reliability.\n\n\n\n\n\n\n\n# License\nMIT\n",
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/SwarmOS',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
