# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['progpysmt',
 'progpysmt.cmd',
 'progpysmt.cmd.installers',
 'progpysmt.smtlib',
 'progpysmt.smtlib.parser',
 'progpysmt.solvers',
 'progpysmt.test',
 'progpysmt.test.smtlib',
 'progpysmt.walkers']

package_data = \
{'': ['*']}

install_requires = \
['cython>=3.0.8,<4.0.0']

setup_kwargs = {
    'name': 'progpysmt',
    'version': '0.1.0',
    'description': 'A Python parser for SMT-LIB, SyGuS and ProgSynth formats.',
    'long_description': '# progpysmt - A SMT-LIB, SyGuS and ProgSynth parser\n\nThis repository is a modification of [pySMT: a Python API for SMT](https://github.com/pysmt/pysmt). The goal of this project is to extend the parser in order to accept the [SyGuS](https://sygus-org.github.io/) format and adapts the output to the [ProgSynth](https://github.com/nathanael-fijalkow/ProgSynth/tree/main) format. \n\n# Usage\nIn order to use the SMT-LIB parser from the original `pySMT` repository, please follow the instructions on their personal github. \nIn order to use the parser on a given file of name `file_name`:\n```Python\nfrom  progpysmt.smtlib.parser  import  ProgSmtLibParser\nfrom  progpysmt.pslobject  import  PSLObject\n\nparser = ProgSmtLibParser()\nwith open(file_name) as f:\n\tpslobject = parser.get_script(f, file_name)\n```   \nThis will create a `PSLObject` that contains all the values required to use ProgSynth.\n\n# Installation\n## From source\nIf you install this from source, you will need Python 3.7 or higher.\n## Poetry\n \n',
    'author': 'Gaëtan MARGUERITTE',
    'author_email': 'gamargueritte@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
