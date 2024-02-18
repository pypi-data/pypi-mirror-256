# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smartq_llm_app_utils']

package_data = \
{'': ['*']}

install_requires = \
['langchain-community>=0.0.16,<0.0.17',
 'langchain-openai>=0.0.5,<0.0.6',
 'langchain>=0.1.4,<0.2.0',
 'pydantic-settings>=2.1.0,<3.0.0',
 'pytest>=8.0.0,<9.0.0']

setup_kwargs = {
    'name': 'smartq-llm-app-utils',
    'version': '0.0.1.post1708003859',
    'description': '',
    'long_description': '',
    'author': 'hwacom_sc_rd2',
    'author_email': 'aiot.hwacom@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
